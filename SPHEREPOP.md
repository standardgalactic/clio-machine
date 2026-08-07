# Spherepop Semantic Reference

This document defines the semantic foundation of Spherepop. It is authoritative for all implementations in this repository.

Implementations may improve algorithms, storage formats, testing, or performance, but they must preserve the semantics described here.

---

# Purpose

Spherepop is not a graph library, stack machine, database, or event sourcing framework.

It is an experimental computational substrate in which computation is represented as transformations of persistent distinctions.

The implementation should therefore prioritize semantic correctness over implementation convenience.

---

# Design Philosophy

Nothing is deleted.

Nothing is overwritten.

Everything remains part of the historical record.

Every computation produces additional history.

History is append-only.

Representations evolve by adding new distinctions rather than mutating previous ones.

---

# Primitive Operations

Spherepop consists of four primitive operations.

These primitives are fundamental.

Do not replace them with alternative terminology.

Do not rename them for stylistic reasons.

---

## Pop

Pop introduces a distinction.

A Pop creates a persistent historical object.

It never modifies existing history.

Pop establishes existence.

---

## Bind

Bind establishes a relationship between existing distinctions.

Binding never destroys either participant.

Bindings may themselves become distinguishable objects.

Bindings are first-class historical entities.

---

## Refuse

Refuse records that a distinction is not admitted into some continuation.

Refusal is informational.

Refusal is not deletion.

The refused distinction remains part of history.

Future computation may still reference it.

---

## Collapse

Collapse records the creation of a new representation.

Collapse does not erase its parents.

Collapse records that multiple distinctions have been incorporated into a new historical distinction.

The precise mathematical semantics of Collapse remain an active research topic.

Implementations should therefore avoid assuming Collapse is merely evaluation, reduction, garbage collection, or simplification.

---

# History

History is append-only.

Every operation appends exactly one historical event.

Historical identifiers are immutable.

Previous events are never modified.

Previous events are never reordered.

---

# Frontier

The frontier represents distinctions currently available for continuation.

Operations may change the frontier.

Operations never change historical events.

Frontier state is derived.

History is primary.

---

# Persistence

Persistent storage exists only to preserve history.

Changing storage technology must not change semantics.

JSON, SQL, binary formats, or databases are implementation details.

---

# Computation

Programs execute by constructing history.

Execution is therefore historical rather than imperative.

The historical trace is the primary computational artifact.

Outputs are derived observations.

---

# Forth Layer

The Forth implementation is an experiment built on Spherepop.

Spherepop is not defined by Forth.

Future languages should be able to use the same primitives without modification.

---

# Agent Guidance

When extending this repository:

Preserve append-only history.

Prefer adding new historical events instead of mutating state.

Avoid introducing hidden mutable state.

Avoid optimizing away history.

Do not rename semantic primitives.

Do not reinterpret primitives according to conventional programming terminology.

If the intended semantics are unclear, preserve existing behavior and leave a documented TODO rather than inventing new semantics.

---

# Preferred Direction

Future work is expected to include:

- admissibility
- continuation
- repair
- provenance
- branching histories
- temporal reasoning
- algebraic semantics
- categorical interpretations
- multiple computational frontiers

These additions should extend the primitive algebra rather than replacing it.

---

# Guiding Principle

A computation is not the destruction of previous representations.

A computation is the construction of richer historical structure.
