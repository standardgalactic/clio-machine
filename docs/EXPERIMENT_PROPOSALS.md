# CLIO Experiment Proposals

These proposals convert speculative roadmap ideas into scoped artifacts with explicit success criteria.

## Global gate for all experiments

Before starting any experiment below:

1. CI must pass (`python -m unittest discover -s tests -p "test_*.py"` and `make check`).
2. Invariant regression coverage must pass for append-only history, immutable identifiers, and frontier behavior.
3. No experiment may redefine primitive semantics in `/home/runner/work/clio-machine/clio-machine/docs/INVARIANTS.md`.

## Proposal 1: Richer event metadata

### Objective

Add optional event metadata fields (timestamps, provenance, admissibility hints) without altering primitive semantics.

### Scope

- Extend event serialization format to include metadata envelope.
- Preserve backward compatibility for existing history files.
- Expose metadata in trace and JSONL outputs.

### Out of scope

- Semantic reinterpretation of `Pop`, `Bind`, `Refuse`, or `Collapse`.
- Storage-engine migration beyond current JSON persistence.

### Success criteria

- Existing tests continue to pass unchanged.
- New tests verify metadata round-trip persistence and trace visibility.
- Histories without metadata remain valid and loadable.

## Proposal 2: Branching or multi-frontier history views

### Objective

Represent multiple continuation frontiers while keeping append-only event history immutable.

### Scope

- Define a view-layer model for named or contextual frontiers.
- Keep canonical event list as single append-only sequence.
- Add tests for frontier projection and consistency.

### Out of scope

- Event deletion, rewrite, or identifier reuse.
- Divergent primitive semantics by frontier.

### Success criteria

- Parent-link validity remains stable across all frontier views.
- Frontier-view tests demonstrate deterministic reconstruction from history.
- Existing single-frontier behavior remains available and compatible.

## Proposal 3: Alternative execution models

### Objective

Prototype new execution consumers that emit Spherepop events while depending on existing primitive layers.

### Scope

- Implement execution models as upper-layer consumers only.
- Require event-history traces as primary artifact.
- Add integration tests comparing emitted invariants across models.

### Out of scope

- Changes that bypass history emission.
- Redefinition of primitive operation names or contracts.

### Success criteria

- Each model emits append-only histories that satisfy invariant tests.
- Cross-model integration tests verify parent-link and frontier consistency.
- Architecture docs remain valid: lower layers are not redefined by consumers.
