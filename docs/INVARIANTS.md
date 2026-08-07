# CLIO Invariants

This document defines semantic contracts that all implementations in this repository must preserve.

## Core history invariants

1. **Append-only history**
   - New operations append events to history.
   - Existing events are never deleted or rewritten.

2. **Immutable identifiers**
   - Event indices are stable once assigned.
   - References to parent events remain valid over time.

3. **No mutation of prior events**
   - Operations may update frontier state.
   - Operations must not mutate historical event records.

4. **Computation as history transformation**
   - All meaningful state transitions are representable as events and frontier updates.

## Primitive-level invariants

1. **Pop**
   - Creates a new event with value payload.
   - Adds the new event to frontier.

2. **Bind**
   - Creates a new event that references two existing parent events.
   - Parent links must remain explicit in the event record.

3. **Refuse**
   - Requires exactly one existing target event index.
   - Records refusal as a new `REFUSE` event with `parents=(target,)`.
   - Stores refusal payload including target and reason metadata.
   - Removes the target from frontier if present.
   - Must not delete or mutate the target event in history.

4. **Collapse**
   - Requires at least one existing target event index.
   - Produces a new `COLLAPSE` event with ordered parent links matching target order.
   - Removes each target from frontier if present.
   - Adds the collapse event to frontier as a new available distinction.
   - Must not mutate target events.

## Pull request policy

Every semantic change should include or update tests that demonstrate continued compliance with these invariants.
