# clio-machine

Constraint-Linked Inference Optimizer (CLIO)

This repository implements the bottom of the CLIO experimental ladder:

```
Spherepop primitives
-> history machine
-> Forth machine
```

The current implementation is intentionally small and append-only:

- `spherepop/` defines `Pop`, `Refuse`, `Bind`, and `Collapse` over persistent history.
- `bin/spherepop` provides a Bash-friendly CLI for recording and inspecting history.
- `forth/` provides a tiny Forth compiler + VM whose execution is realized through
  Spherepop events.
- `spherepop_blender/` + `scenes/` provide a Blender visualization suite for
  persistent Spherepop event histories.

The manuscript now follows a standardized modular chapter scaffold with shared
`common/` reusable content, chapter metadata, and a generated prerequisite graph.

## Research protocol docs

- `/home/runner/work/clio-machine/clio-machine/COPILOT.md` defines contributor context for coding agents.
- `/home/runner/work/clio-machine/clio-machine/docs/INVARIANTS.md` defines semantic contracts.
- `/home/runner/work/clio-machine/clio-machine/docs/ARCHITECTURE.md` describes repository layers.
- `/home/runner/work/clio-machine/clio-machine/docs/ROADMAP.md` separates foundation, active focus, and experiments.
- `/home/runner/work/clio-machine/clio-machine/docs/GLOSSARY.md` defines project terms.
- `/home/runner/work/clio-machine/clio-machine/docs/CONTRIBUTING.md` defines human and AI contribution rules.
- `/home/runner/work/clio-machine/clio-machine/agents/project_context.md` provides a concise machine-oriented prompt.
- `/home/runner/work/clio-machine/clio-machine/SPHEREPOP_BLENDER_SUITE.md` documents the Blender scene suite and headless render scripts.

## Quick start

```bash
bin/spherepop pop 5
bin/spherepop pop 8
bin/spherepop bind 0 1
bin/spherepop collapse 2
bin/spherepop trace
```

```bash
bin/forth "2 3 + ."
```

Use `SPHEREPOP_STATE_PATH` to control where history is persisted.

## Manuscript scaffold checks

```bash
make check
```

This validates labels, chapter scaffold consistency, and dependency graph drift.

## Tests

Run all tests:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

Invariant-focused regression coverage lives in:

- `/home/runner/work/clio-machine/clio-machine/tests/test_semantic_invariants.py`

## Canonical local verification (matches CI)

Run the same verification sequence used by the CI workflow before opening a pull request:

```bash
python -m unittest discover -s tests -p "test_*.py"
make check
```
