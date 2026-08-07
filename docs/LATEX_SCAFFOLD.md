# CLIO LaTeX Scaffold

This repository now includes a software-style manuscript scaffold for a long-form CLIO volume.

## Build commands

- `make all` — generate reproducible figures, run manuscript checks, compile full volume.
- `make quick` — compile quickly in nonstop mode.
- `make figures` — regenerate deterministic figure artifacts.
- `make check` — run label-uniqueness checks.

## Layout

- `clio.tex` master document
- `styles/` modular style packages
- `frontmatter/`, `parts/`, `appendices/`, `backmatter/`
- `bibliography/` domain-separated BibLaTeX files
- `figures/static` and `figures/generated`
- `scripts/manuscript/` reproducibility and validation scripts

Each chapter/appendix has its own directory with local `figures/`, `simulations/`, `tables/`, `exercises/`, `notes/`, and `code/` folders.
