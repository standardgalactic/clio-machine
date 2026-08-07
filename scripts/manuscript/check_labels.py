#!/usr/bin/env python3
"""Check duplicate LaTeX labels across manuscript sources."""

from __future__ import annotations

import argparse
import re
from collections import defaultdict
from pathlib import Path

LABEL = re.compile(r"\\label\{([^}]+)\}")


def tex_files(root: Path):
    for path in root.rglob("*.tex"):
        if ".git" in path.parts or "build" in path.parts:
            continue
        yield path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    hits = defaultdict(list)

    for path in tex_files(root):
        content = path.read_text(encoding="utf-8")
        for idx, line in enumerate(content.splitlines(), start=1):
            for label in LABEL.findall(line):
                hits[label].append((path.relative_to(root), idx))

    duplicates = {k: v for k, v in hits.items() if len(v) > 1}
    if duplicates:
        print("Duplicate labels found:")
        for key, refs in sorted(duplicates.items()):
            print(f"  {key}")
            for ref in refs:
                print(f"    - {ref[0]}:{ref[1]}")
        return 1

    print(f"Checked {len(list(tex_files(root)))} TeX files; no duplicate labels found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
