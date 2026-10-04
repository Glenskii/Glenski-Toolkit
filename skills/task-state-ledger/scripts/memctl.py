#!/usr/bin/env python3
"""Project memory helper: ROADMAP.md, PROJECT-LOG.md and an append-only archive.

Usage:
    python memctl.py init [--root DIR] [--integrate]
    python memctl.py log --title T --asked A --decided D --why W --shipped S [--root DIR] [--dry-run]
    python memctl.py rotate [--root DIR] [--dry-run]
    python memctl.py status [--root DIR]

Python 3.10+, standard library only. All files are UTF-8 with LF line endings.
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import sys
import tempfile
from pathlib import Path

# ---- Constants -------------------------------------------------------------

MAX_ENTRIES = 15
MAX_LOG_BYTES = 6000
ROADMAP_NAME = "ROADMAP.md"
LOG_NAME = "PROJECT-LOG.md"
ARCHIVE_REL = Path("docs") / "PROJECT-LOG-ARCHIVE.md"
TEMPLATE_DIR = Path(__file__).resolve().parents[1] / "templates"
ENTRY_HEADING = re.compile(r"^## \d{4}-\d{2}-\d{2} - .+$")
FIELDS = ("asked", "decided", "why", "shipped")
MARKER_BEGIN = "<!-- project-memory:begin -->"
MARKER_END = "<!-- project-memory:end -->"

ARCHIVE_HEADER = (
    "# Project Log Archive\n\n"
    "Append-only. Entries rotated out of PROJECT-LOG.md are stored here unchanged, oldest first. "
    "Do not edit or delete entries.\n"
)

INTEGRATION_BLOCK = (
    f"{MARKER_BEGIN}\n"
    "## Project memory\n\n"
    "- ROADMAP.md holds Backlog, In Progress and Done. Update it when work starts or finishes.\n"
    "- PROJECT-LOG.md holds durable decisions as 4-line entries. Append with "
    "`python <skill-path>/scripts/memctl.py log --title ... --asked ... --decided ... --why ... --shipped ...`.\n"
    "- Never write secrets, personal data, or client confidential material into these files.\n"
    f"{MARKER_END}\n"
)

# Mirrors the patterns in write_evidence.py.
SENSITIVE_PATTERNS = (
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----", re.IGNORECASE),
    re.compile(r"authorization\s*:\s*bearer\s+\S+", re.IGNORECASE),
    re.compile(
        r"(?:api[_-]?key|access[_-]?token|refresh[_-]?token|password|secret)\s*[:=]\s*['\"]?\S+",
        re.IGNORECASE,
    ),
)


# ---- File helpers ----------------------------------------------------------


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def atomic_write(path: Path, content: str) -> None:
    """Write via a temp file in the same directory, then replace."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(
        dir=path.parent, prefix=path.name + ".", suffix=".tmp"
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, path)
    except BaseException:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


# ---- Log parsing and rendering ---------------------------------------------


def parse_log(text: str) -> tuple[str, list[str]]:
    """Split text into (header, entries). Entry text has no trailing whitespace."""
    lines = text.replace("\r\n", "\n").split("\n")
    header_lines: list[str] = []
    entries: list[list[str]] = []
    for line in lines:
        if ENTRY_HEADING.match(line):
            entries.append([line])
        elif entries:
            entries[-1].append(line)
        else:
            header_lines.append(line)
    return "\n".join(header_lines).rstrip(), ["\n".join(e).rstrip() for e in entries]


def render_log(header: str, entries: list[str]) -> str:
    parts = [header.rstrip()] if header.strip() else []
    parts.extend(entries)
    return "\n\n".join(parts) + "\n"


def plan_rotation(header: str, entries: list[str]) -> tuple[list[str], list[str]]:
    """Return (kept, to_archive). Oldest entries are archived first."""
    split = max(0, len(entries) - MAX_ENTRIES)
    to_archive = entries[:split]
    kept = entries[split:]
    while (
        len(kept) > 1 and len(render_log(header, kept).encode("utf-8")) > MAX_LOG_BYTES
    ):
        to_archive.append(kept.pop(0))
    return kept, to_archive


def entry_title(entry: str) -> str:
    return entry.split("\n", 1)[0][3:]


# ---- Validation ------------------------------------------------------------


def clean_field(name: str, value: str) -> str:
    cleaned = " ".join(value.split())
    if not cleaned:
        raise ValueError(f"Field '{name}' must not be empty.")
    if any(p.search(cleaned) for p in SENSITIVE_PATTERNS):
        raise ValueError(
            f"Field '{name}' appears to contain sensitive material. Redact it first."
        )
    return cleaned


def build_entry(
    title: str,
    asked: str,
    decided: str,
    why: str,
    shipped: str,
    today: dt.date | None = None,
) -> str:
    date = (today or dt.date.today()).isoformat()
    values = {
        "title": clean_field("title", title),
        "asked": clean_field("asked", asked),
        "decided": clean_field("decided", decided),
        "why": clean_field("why", why),
        "shipped": clean_field("shipped", shipped),
    }
    lines = [f"## {date} - {values['title']}"] + [f"{f}: {values[f]}" for f in FIELDS]
    return "\n".join(lines)


# ---- Commands --------------------------------------------------------------


def do_rotate(root: Path, dry_run: bool) -> str:
    log_path = root / LOG_NAME
    if not log_path.is_file():
        raise ValueError(f"{LOG_NAME} not found in {root}. Run init first.")
    header, entries = parse_log(read_text(log_path))
    kept, to_archive = plan_rotation(header, entries)
    if not to_archive:
        return f"Rotate: nothing to archive ({len(entries)} active entries)."
    message = f"Rotate: archived {len(to_archive)} entries, kept {len(kept)}."
    if dry_run:
        return "[dry-run] " + message
    archive_path = root / ARCHIVE_REL
    archive_text = read_text(archive_path) if archive_path.is_file() else ARCHIVE_HEADER
    existing = set(parse_log(archive_text)[1])
    new_entries = [e for e in to_archive if e not in existing]
    if new_entries:
        atomic_write(
            archive_path,
            archive_text.rstrip() + "\n\n" + "\n\n".join(new_entries) + "\n",
        )
    # Archive is written first, so a crash between writes only causes a deduplicated retry.
    atomic_write(log_path, render_log(header, kept))
    return message


def do_log(root: Path, entry: str, dry_run: bool) -> list[str]:
    log_path = root / LOG_NAME
    if not log_path.is_file():
        raise ValueError(f"{LOG_NAME} not found in {root}. Run init first.")
    header, entries = parse_log(read_text(log_path))
    if dry_run:
        kept, to_archive = plan_rotation(header, entries + [entry])
        return [
            "[dry-run] Would append:",
            entry,
            f"[dry-run] Rotation would archive {len(to_archive)} entries, keep {len(kept)}.",
        ]
    atomic_write(log_path, render_log(header, entries + [entry]))
    return [f"Appended: {entry_title(entry)}", do_rotate(root, False)]


def read_template(name: str) -> str:
    path = TEMPLATE_DIR / name
    if not path.is_file():
        raise ValueError(f"Template missing: {path}")
    return read_text(path)


def do_init(root: Path, integrate: bool) -> list[str]:
    if not root.is_dir():
        raise ValueError(f"Root directory does not exist: {root}")
    out: list[str] = []
    targets = (
        (root / ROADMAP_NAME, "roadmap-template.md"),
        (root / LOG_NAME, "project-log-template.md"),
        (root / ARCHIVE_REL, None),
    )
    for path, template in targets:
        rel = path.relative_to(root).as_posix()
        if path.exists():
            out.append(f"Exists, left unchanged: {rel}")
            continue
        atomic_write(path, read_template(template) if template else ARCHIVE_HEADER)
        out.append(f"Created: {rel}")
    if integrate:
        for name in ("CLAUDE.md", "AGENTS.md"):
            path = root / name
            if not path.is_file():
                out.append(
                    f"Skipped {name}: file does not exist (never created by this tool)"
                )
                continue
            text = read_text(path)
            if MARKER_BEGIN in text:
                out.append(f"Skipped {name}: block already present")
                continue
            atomic_write(path, text.rstrip("\n") + "\n\n" + INTEGRATION_BLOCK)
            out.append(f"Appended block to {name}")
    else:
        out.append(
            "Add this block to CLAUDE.md or AGENTS.md if you want agents to follow it:"
        )
        out.append(INTEGRATION_BLOCK.rstrip())
    return out


def in_progress_items(roadmap_text: str) -> list[str]:
    items: list[str] = []
    active = False
    for line in roadmap_text.splitlines():
        if line.startswith("## "):
            active = line[3:].strip().lower() == "in progress"
            continue
        if active and line.strip():
            items.append(line.strip())
    return items


def do_status(root: Path) -> list[str]:
    out: list[str] = []
    roadmap = root / ROADMAP_NAME
    if roadmap.is_file():
        items = in_progress_items(read_text(roadmap))
        out.append(f"In Progress ({len(items)}):")
        out.extend(f"  {i}" for i in items) if items else out.append("  none")
    else:
        out.append(f"{ROADMAP_NAME}: missing (run init)")
    log = root / LOG_NAME
    if log.is_file():
        _, entries = parse_log(read_text(log))
        out.append(f"Active log entries: {len(entries)}")
        out.append("Last 3 entries:")
        out.extend(
            f"  {entry_title(e)}" for e in entries[-3:]
        ) if entries else out.append("  none")
    else:
        out.append(f"{LOG_NAME}: missing (run init)")
    return out


# ---- CLI -------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Project roadmap and decision log helper."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    def add_root(p: argparse.ArgumentParser) -> None:
        p.add_argument(
            "--root",
            type=Path,
            default=Path.cwd(),
            help="Repository root (default: current directory)",
        )

    p_init = sub.add_parser("init", help="Create memory files without overwriting")
    add_root(p_init)
    p_init.add_argument(
        "--integrate",
        action="store_true",
        help="Append the marked block to an existing CLAUDE.md/AGENTS.md",
    )

    p_log = sub.add_parser("log", help="Append one decision entry")
    add_root(p_log)
    for field in ("title",) + FIELDS:
        p_log.add_argument(f"--{field}", required=True)
    p_log.add_argument("--dry-run", action="store_true")

    p_rot = sub.add_parser("rotate", help="Archive oldest entries beyond the limits")
    add_root(p_rot)
    p_rot.add_argument("--dry-run", action="store_true")

    p_status = sub.add_parser(
        "status", help="Show in-progress items and recent log titles"
    )
    add_root(p_status)
    return parser


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, OSError):
            pass
    args = build_parser().parse_args(argv)
    root = args.root.resolve()
    try:
        if args.command == "init":
            lines = do_init(root, args.integrate)
        elif args.command == "log":
            entry = build_entry(
                args.title, args.asked, args.decided, args.why, args.shipped
            )
            lines = do_log(root, entry, args.dry_run)
        elif args.command == "rotate":
            lines = [do_rotate(root, args.dry_run)]
        else:
            lines = do_status(root)
    except (OSError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
