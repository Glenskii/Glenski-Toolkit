#!/usr/bin/env python3
"""Verify local Markdown links and images in public skill documentation."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+['\"][^)]*['\"])?\)")
SKIP_PREFIXES = ("#", "http://", "https://", "mailto:", "tel:")


def local_target(markdown_file: Path, destination: str) -> Path | None:
    destination = unquote(destination.strip("<>"))
    if destination.startswith(SKIP_PREFIXES):
        return None
    path_text = destination.split("#", 1)[0].split("?", 1)[0]
    if not path_text:
        return None
    return (markdown_file.parent / path_text).resolve()


def main() -> int:
    missing: list[str] = []
    checked = 0

    for markdown_file in sorted((ROOT / "skills").glob("*/**/*.md")):
        text = markdown_file.read_text(encoding="utf-8")
        for match in LINK_PATTERN.finditer(text):
            target = local_target(markdown_file, match.group(1))
            if target is None:
                continue
            checked += 1
            if not target.exists():
                missing.append(
                    f"{markdown_file.relative_to(ROOT)} -> {match.group(1)}"
                )

    if missing:
        print("Broken local documentation links:")
        print("\n".join(f"- {item}" for item in missing))
        return 1

    print(f"PASS: checked {checked} local Markdown links and images.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
