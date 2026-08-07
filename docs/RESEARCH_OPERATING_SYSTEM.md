# CLIO Research Operating System Layout

The repository now supports a research-OS style scaffold so the book is one projection of a broader program.

## Textbook view

- `clio.tex` and `parts/` provide the monograph build.
- `common/` stores reusable chapter modules.
- `docs/chapter-dependencies.json` is the prerequisite graph source.

## Execution and simulation view

- `simulations/` stores deterministic simulation families used for figures.
- `examples/` stores executable examples separated by pedagogical intent.
- `figures/generated/` stores generated artifacts.

## Program-level workspace view

Scaffold roots are available for cross-medium outputs:

- `book/`
- `papers/`
- `experiments/`
- `python/`
- `rust/`
- `blender/`
- `datasets/`
- `benchmarks/`
- `lectures/`
- `slides/`
- `videos/`
- `notes/`
- `website/`

These roots are intentionally lightweight until specific pipelines are attached.
