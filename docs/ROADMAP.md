# CLIO Roadmap

## Completed foundation

- Spherepop primitive operations (`Pop`, `Bind`, `Refuse`, `Collapse`)
- Append-only history model with frontier tracking
- State persistence and trace rendering
- Basic CLI for history operations
- Minimal Forth compiler + VM as a semantic consumer

## Active focus

- Strengthen invariant-driven regression tests
- Clarify semantic expectations for `Collapse` and `Refuse`
- Improve documentation that guides AI and human contributors

## Speculative experiments

- Richer event metadata (timestamps, provenance, admissibility fields)
- Branching or multi-frontier history views
- Alternative execution models over the same primitive substrate

## Long-term goals

- Treat the repository as executable specification of the underlying theory
- Increase formal alignment between implementation behavior and research semantics
- Make semantic regressions easier to detect than implementation regressions
