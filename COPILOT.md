# CLIO Copilot Context

## Project type

CLIO is an executable research project, not a production CRUD application.
Code quality matters, but semantic correctness comes first.

## Spherepop primitives are semantic primitives

`Pop`, `Bind`, `Refuse`, and `Collapse` are first-class conceptual operations.
Do not rename them or replace them with generic graph/stack terminology.

## Expected contribution behavior

Before changing code:

1. Identify the invariant affected by the change.
2. Preserve append-only event history and immutable event identifiers.
3. Avoid mutating prior events.
4. Explain semantic impact in tests and commit messages.

When uncertain about theory-level semantics, prefer explicit TODO notes over invented behavior.

## Required support for new primitives

Any new primitive introduced to this repository must include:

- documentation
- unit tests
- trace representation
- persistence support
