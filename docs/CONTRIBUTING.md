# Contributing to CLIO

## Purpose

This repository is an executable research project.
Contributions should preserve semantic contracts before optimizing implementation details.

## Environment prerequisites

- Python 3.11+
- GNU Make

## Canonical verification runbook

Use this exact sequence locally before opening a pull request:

1. `python -m unittest discover -s tests -p "test_*.py"`
2. `make check`

This runbook matches the repository CI workflow.

## Rules for all contributors

1. Preserve append-only history semantics.
2. Do not rename or redefine `Pop`, `Bind`, `Refuse`, or `Collapse`.
3. Prefer extending existing abstractions over introducing parallel mutable models.
4. Add or update tests for every semantic change.
5. Explain which invariant a change affects in pull request descriptions.

## Additional rules for AI-generated changes

1. Treat `/home/runner/work/clio-machine/clio-machine/docs/INVARIANTS.md` as normative.
2. When uncertain about semantics, leave explicit TODO markers rather than inventing behavior.
3. Keep changes local and reversible.
4. Avoid style-only refactors that obscure primitive semantics.

## Contribution guardrails

- Read `/home/runner/work/clio-machine/clio-machine/docs/INVARIANTS.md` first and identify the invariant touched by your change.
- Confirm the layer impact using `/home/runner/work/clio-machine/clio-machine/docs/ARCHITECTURE.md` so higher layers do not redefine primitive semantics.
- Validate roadmap alignment against `/home/runner/work/clio-machine/clio-machine/docs/ROADMAP.md` before expanding scope.
- Prefer adding semantic tests over broad refactors when behavior changes.

## Required artifacts for new primitives

Any new primitive must include:

- user-facing documentation
- unit tests covering invariant behavior
- trace output support
- persistence serialization/deserialization support
