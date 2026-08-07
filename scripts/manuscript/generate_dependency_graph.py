#!/usr/bin/env python3
"""Generate a chapter dependency graph TeX include from JSON metadata."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

POS = {
    1: (0, 0),
    2: (2, -2),
    3: (0, -4),
    4: (4, -4),
    5: (2, -6),
    6: (2, -8),
    7: (2, -10),
    8: (2, -12),
    9: (0, -14),
    10: (2, -16),
    11: (4, -18),
    12: (0, -20),
    13: (2, -22),
    14: (2, -24),
}


def render(chapters: list[dict]) -> str:
    lines: list[str] = []
    lines.append(r"\section*{Chapter Dependency Graph}")
    lines.append("")
    lines.append("The dependency graph below encodes prerequisite flow for the textbook sequence.")
    lines.append("")
    lines.append(r"\begin{center}")
    lines.append(r"\begin{tikzpicture}[x=1.6cm,y=0.6cm]")

    for ch in chapters:
        idx = ch["id"]
        x, y = POS[idx]
        title = ch["title"].replace("&", r"\&")
        lines.append(
            rf"\node[clio-node] (ch{idx}) at ({x},{y}) {{Chapter {idx}\\{title}}};"
        )

    lines.append("")
    for ch in chapters:
        idx = ch["id"]
        for prereq in ch["prerequisites"]:
            lines.append(rf"\draw[clio-arrow] (ch{prereq}) -- (ch{idx});")

    lines.append(r"\end{tikzpicture}")
    lines.append(r"\end{center}")
    lines.append("")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    src = root / "docs" / "chapter-dependencies.json"
    out = root / "frontmatter" / "chapter-dependency-graph.tex"

    payload = json.loads(src.read_text(encoding="utf-8"))
    chapters = sorted(payload["chapters"], key=lambda c: c["id"])
    rendered = render(chapters)

    if args.check:
        existing = out.read_text(encoding="utf-8") if out.exists() else ""
        if existing != rendered:
            print("Dependency graph include is out of date. Run generate_dependency_graph.py.")
            return 1
        print("Dependency graph include is up to date.")
        return 0

    out.write_text(rendered, encoding="utf-8")
    print(f"Wrote {out.relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
