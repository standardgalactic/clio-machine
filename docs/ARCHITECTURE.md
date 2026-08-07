# CLIO Architecture

CLIO is layered to keep semantic primitives stable while allowing experimental consumers.

## Layer 1: Spherepop primitives

Location: `/home/runner/work/clio-machine/clio-machine/spherepop/`

This layer defines the primitive operations and event-history substrate.
It is the semantic base of the repository.

## Layer 2: History substrate

Location: `/home/runner/work/clio-machine/clio-machine/spherepop/history.py`

This layer implements append-only event storage, parent links, and frontier tracking.
Persistence and trace rendering depend on this model.

## Layer 3: Experimental execution model (Forth VM)

Location: `/home/runner/work/clio-machine/clio-machine/forth/`

The Forth machine is a consumer of Spherepop.
It should express execution by emitting Spherepop events rather than bypassing history.

## Extension rule

New languages, interpreters, or execution models should depend downward on lower layers.
They should not redefine lower-layer primitive semantics.
