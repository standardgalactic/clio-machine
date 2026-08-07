# CLIO LaTeX Scaffold

This repository now includes a software-engineered manuscript scaffold for a long-form CLIO volume.

## Build commands

- `make all` — generate reproducible figures, run manuscript checks, compile full volume.
- `make quick` — compile quickly in nonstop mode.
- `make figures` — regenerate deterministic figure artifacts.
- `make check` — run label checks, chapter scaffold validation, and dependency-graph drift checks.

## Layout

- `clio.tex` master document
- `styles/` modular style packages
- `frontmatter/`, `parts/`, `appendices/`, `backmatter/`
- `bibliography/` domain-separated BibLaTeX files
- `figures/static` and `figures/generated`
- `scripts/manuscript/` reproducibility and validation scripts
- `common/` reusable notation, proof, theorem-style, and sidebar modules
- `docs/chapter-dependencies.json` chapter prerequisite graph source

## Standard chapter contract

Every chapter in `parts/**/ch*/` follows the same internal rhythm and file contract:

1. `metadata`
2. `preface`
3. `historical-motivation`
4. `central-question`
5. `conceptual-overview`
6. `formal-definitions`
7. `worked-examples`
8. `mathematical-development`
9. `major-derivations`
10. `theorems`
11. `proofs`
12. `counterexamples`
13. `computational-interpretation`
14. `algorithms`
15. `engineering-notes`
16. `connections`
17. `exercises`
18. `research-problems`
19. `summary`
20. `notation`

Each chapter directory also includes local `figures/`, `simulations/`, `code/`, `notes/`, `tables/`, and `exercise-assets/` folders.
