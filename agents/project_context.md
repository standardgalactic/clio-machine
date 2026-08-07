You are contributing to CLIO.

This repository is an executable research project rather than a production application.

Your objective is to preserve semantic correctness before improving implementation quality.

Before modifying code, identify which invariant your change affects.

Never redefine Spherepop primitives (`Pop`, `Bind`, `Refuse`, `Collapse`).

Prefer extending the history model over introducing mutable state.

When uncertain, leave TODO comments rather than inventing semantics.

Every new primitive must include:
- documentation
- unit tests
- trace representation
- persistence support
