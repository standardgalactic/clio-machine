# clio-machine

Constraint-Linked Inference Organiser (CLIO)

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
