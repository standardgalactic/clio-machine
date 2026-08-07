#!/usr/bin/env python3
"""Validate chapter scaffold consistency for CLIO manuscript."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REQUIRED_FILES = [
    "chapter.tex",
    "metadata.tex",
    "metadata.json",
    "preface.tex",
    "historical-motivation.tex",
    "central-question.tex",
    "conceptual-overview.tex",
    "formal-definitions.tex",
    "worked-examples.tex",
    "mathematical-development.tex",
    "major-derivations.tex",
    "theorems.tex",
    "proofs.tex",
    "counterexamples.tex",
    "computational-interpretation.tex",
    "algorithms.tex",
    "engineering-notes.tex",
    "connections.tex",
    "exercises.tex",
    "research-problems.tex",
    "summary.tex",
    "notation.tex",
    "bibliography.bib",
]

REQUIRED_DIRS = ["figures", "simulations", "code", "notes", "tables", "exercise-assets"]

INPUT_ORDER = [
    "metadata",
    "preface",
    "historical-motivation",
    "central-question",
    "conceptual-overview",
    "formal-definitions",
    "worked-examples",
    "mathematical-development",
    "major-derivations",
    "theorems",
    "proofs",
    "counterexamples",
    "computational-interpretation",
    "algorithms",
    "engineering-notes",
    "connections",
    "exercises",
    "research-problems",
    "summary",
    "notation",
]

INPUT_RE = re.compile(r"\\input\{([^}]+)\}")


def chapter_dirs(parts_root: Path):
    for path in sorted(parts_root.glob("**/ch*")):
        if path.is_dir():
            yield path


def validate_chapter(chdir: Path, root: Path) -> list[str]:
    errs: list[str] = []
    rel = chdir.relative_to(root)

    for name in REQUIRED_FILES:
        if not (chdir / name).is_file():
            errs.append(f"{rel}: missing file {name}")

    for name in REQUIRED_DIRS:
        if not (chdir / name).is_dir():
            errs.append(f"{rel}: missing directory {name}")

    chapter_tex = chdir / "chapter.tex"
    if chapter_tex.exists():
        txt = chapter_tex.read_text(encoding="utf-8")
        inputs = [x.split("/")[-1] for x in INPUT_RE.findall(txt)]
        if inputs != INPUT_ORDER:
            errs.append(f"{rel}: chapter input order mismatch")

    metadata_json = chdir / "metadata.json"
    if metadata_json.exists():
        try:
            data = json.loads(metadata_json.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errs.append(f"{rel}: invalid metadata.json ({exc})")
            return errs

        required_keys = {
            "chapter",
            "slug",
            "title",
            "part",
            "prerequisites",
            "mathematics",
            "software",
            "estimated_reading",
            "exercise_count",
            "proof_count",
            "derivation_count",
        }
        missing = sorted(required_keys - set(data))
        if missing:
            errs.append(f"{rel}: metadata missing keys {missing}")
        if data.get("slug") != chdir.name:
            errs.append(f"{rel}: metadata slug does not match directory name")
        if not isinstance(data.get("prerequisites", []), list):
            errs.append(f"{rel}: metadata prerequisites must be a list")

    return errs


def validate_dependencies(root: Path, chapters: list[Path]) -> list[str]:
    errs: list[str] = []
    dep_file = root / "docs" / "chapter-dependencies.json"
    if not dep_file.exists():
        return ["docs/chapter-dependencies.json: missing dependency map"]

    data = json.loads(dep_file.read_text(encoding="utf-8"))
    items = data.get("chapters", [])
    ids = {item["id"] for item in items}

    chapter_numbers = set()
    for ch in chapters:
        meta = ch / "metadata.json"
        if meta.exists():
            chapter_numbers.add(json.loads(meta.read_text(encoding="utf-8"))["chapter"])

    missing = sorted(chapter_numbers - ids)
    if missing:
        errs.append(f"docs/chapter-dependencies.json: missing chapter ids {missing}")

    for item in items:
        cid = item["id"]
        for prereq in item.get("prerequisites", []):
            if prereq not in ids:
                errs.append(
                    f"docs/chapter-dependencies.json: chapter {cid} references unknown prerequisite {prereq}"
                )
            if prereq >= cid:
                errs.append(
                    f"docs/chapter-dependencies.json: chapter {cid} has non-earlier prerequisite {prereq}"
                )

    return errs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    parts_root = root / "parts"
    chapters = list(chapter_dirs(parts_root))

    errors: list[str] = []
    for ch in chapters:
        errors.extend(validate_chapter(ch, root))

    errors.extend(validate_dependencies(root, chapters))

    if errors:
        print("Scaffold validation failed:")
        for err in errors:
            print(f"  - {err}")
        return 1

    print(f"Validated {len(chapters)} chapter scaffolds and dependency metadata.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
