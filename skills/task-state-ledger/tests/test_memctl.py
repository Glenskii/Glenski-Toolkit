from __future__ import annotations

import datetime as dt
import importlib.util
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "memctl.py"
SPEC = importlib.util.spec_from_file_location("memctl", SCRIPT)
assert SPEC and SPEC.loader
memctl = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(memctl)

LOG = "PROJECT-LOG.md"
ARCHIVE = Path("docs") / "PROJECT-LOG-ARCHIVE.md"


def add(root: Path, n: int, pad: str = "") -> None:
    entry = memctl.build_entry(
        f"Decision {n:02d}",
        "asked it",
        "decided it",
        "because " + pad,
        "shipped it",
        today=dt.date(2025, 1, 1),
    )
    header, entries = memctl.parse_log((root / LOG).read_text(encoding="utf-8"))
    (root / LOG).write_text(
        memctl.render_log(header, entries + [entry]), encoding="utf-8"
    )


def titles(path: Path) -> list[str]:
    return [
        memctl.entry_title(e)
        for e in memctl.parse_log(path.read_text(encoding="utf-8"))[1]
    ]


def names(lo: int, hi: int) -> list[str]:
    return [f"2025-01-01 - Decision {n:02d}" for n in range(lo, hi + 1)]


@pytest.fixture()
def root(tmp_path: Path) -> Path:
    assert memctl.main(["init", "--root", str(tmp_path)]) == 0
    return tmp_path


def test_rotate_keeps_newest_15_archives_oldest_in_order(root: Path) -> None:
    for n in range(1, 21):
        add(root, n)
    memctl.do_rotate(root, False)
    assert titles(root / LOG) == names(6, 20)
    assert titles(root / ARCHIVE) == names(1, 5)


def test_size_cap_archives_oldest_never_newest(root: Path) -> None:
    for n in range(1, 11):
        add(root, n, pad="x" * 700)
    memctl.do_rotate(root, False)
    active = titles(root / LOG)
    assert len((root / LOG).read_bytes()) <= memctl.MAX_LOG_BYTES
    assert active[-1].endswith("Decision 10")
    assert titles(root / ARCHIVE) == names(1, 10 - len(active))


def test_single_oversized_entry_is_kept(root: Path) -> None:
    add(root, 1, pad="y" * 7000)
    memctl.do_rotate(root, False)
    assert len(titles(root / LOG)) == 1


def test_second_rotate_is_noop(root: Path) -> None:
    for n in range(1, 21):
        add(root, n)
    memctl.do_rotate(root, False)
    before = ((root / LOG).read_bytes(), (root / ARCHIVE).read_bytes())
    memctl.do_rotate(root, False)
    assert before == ((root / LOG).read_bytes(), (root / ARCHIVE).read_bytes())


def test_archive_append_only_no_loss_or_duplicates(root: Path) -> None:
    for n in range(1, 18):
        add(root, n)
    memctl.do_rotate(root, False)
    first = titles(root / ARCHIVE)
    for n in range(18, 24):
        add(root, n)
    memctl.do_rotate(root, False)
    second = titles(root / ARCHIVE)
    assert second[: len(first)] == first
    assert second + titles(root / LOG) == names(1, 23)


def test_retry_after_partial_crash_does_not_duplicate(root: Path) -> None:
    for n in range(1, 20):
        add(root, n)
    # Simulate a crash after the archive write but before the log write.
    header, entries = memctl.parse_log((root / LOG).read_text(encoding="utf-8"))
    _, to_archive = memctl.plan_rotation(header, entries)
    text = (root / ARCHIVE).read_text(encoding="utf-8")
    (root / ARCHIVE).write_text(
        text.rstrip() + "\n\n" + "\n\n".join(to_archive) + "\n", encoding="utf-8"
    )
    memctl.do_rotate(root, False)
    assert titles(root / ARCHIVE) == names(1, 4)


def test_dry_run_changes_nothing(root: Path) -> None:
    for n in range(1, 20):
        add(root, n)
    snapshot = (root / LOG).read_bytes()
    assert "dry-run" in memctl.do_rotate(root, True)
    assert (root / LOG).read_bytes() == snapshot


def test_init_never_overwrites_and_is_idempotent(tmp_path: Path) -> None:
    (tmp_path / "ROADMAP.md").write_text("mine\n", encoding="utf-8")
    memctl.main(["init", "--root", str(tmp_path)])
    snapshot = {p.name: p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()}
    memctl.main(["init", "--root", str(tmp_path)])
    assert (tmp_path / "ROADMAP.md").read_text(encoding="utf-8") == "mine\n"
    assert snapshot == {
        p.name: p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()
    }
    assert (tmp_path / ARCHIVE).is_file()


def test_integrate_adds_block_once_and_never_creates(tmp_path: Path) -> None:
    (tmp_path / "CLAUDE.md").write_text("# Rules\n", encoding="utf-8")
    memctl.main(["init", "--root", str(tmp_path), "--integrate"])
    memctl.main(["init", "--root", str(tmp_path), "--integrate"])
    text = (tmp_path / "CLAUDE.md").read_text(encoding="utf-8")
    assert text.count(memctl.MARKER_BEGIN) == 1
    assert text.startswith("# Rules\n")
    assert not (tmp_path / "AGENTS.md").exists()


def test_init_without_integrate_leaves_guidance_files_alone(tmp_path: Path) -> None:
    (tmp_path / "AGENTS.md").write_text("x\n", encoding="utf-8")
    memctl.main(["init", "--root", str(tmp_path)])
    assert (tmp_path / "AGENTS.md").read_text(encoding="utf-8") == "x\n"


def test_log_rejects_secret_pattern(root: Path) -> None:
    code = memctl.main(
        [
            "log",
            "--root",
            str(root),
            "--title",
            "T",
            "--asked",
            "a",
            "--decided",
            "set api_key=abc123",
            "--why",
            "w",
            "--shipped",
            "s",
        ]
    )
    assert code == 1
    assert titles(root / LOG) == []


def test_log_rejects_empty_field(root: Path) -> None:
    code = memctl.main(
        [
            "log",
            "--root",
            str(root),
            "--title",
            "T",
            "--asked",
            "  ",
            "--decided",
            "d",
            "--why",
            "w",
            "--shipped",
            "s",
        ]
    )
    assert code == 1
    assert titles(root / LOG) == []


def test_log_missing_file_errors(tmp_path: Path) -> None:
    assert (
        memctl.main(
            [
                "log",
                "--root",
                str(tmp_path),
                "--title",
                "T",
                "--asked",
                "a",
                "--decided",
                "d",
                "--why",
                "w",
                "--shipped",
                "s",
            ]
        )
        == 1
    )


def test_entry_round_trip_exact(root: Path) -> None:
    entry = memctl.build_entry(
        "Use plain files",
        "where",
        "markdown",
        "portable",
        "templates",
        today=dt.date(2025, 2, 3),
    )
    assert entry == (
        "## 2025-02-03 - Use plain files\nasked: where\ndecided: markdown\n"
        "why: portable\nshipped: templates"
    )
    header, _ = memctl.parse_log((root / LOG).read_text(encoding="utf-8"))
    parsed_header, parsed = memctl.parse_log(memctl.render_log(header, [entry]))
    assert parsed == [entry] and parsed_header == header


def test_template_has_no_real_entries(root: Path) -> None:
    assert titles(root / LOG) == []


def test_status_missing_files_exit_zero(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert memctl.main(["status", "--root", str(tmp_path)]) == 0
    assert "missing" in capsys.readouterr().out


def test_status_reports_in_progress_and_last_three(
    root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    for n in range(1, 6):
        add(root, n)
    memctl.main(["status", "--root", str(root)])
    out = capsys.readouterr().out
    assert "In Progress (1)" in out and "Active log entries: 5" in out
    assert "Decision 05" in out and "Decision 03" in out and "Decision 02" not in out
