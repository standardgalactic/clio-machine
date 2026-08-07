# CLIO Glossary

## Pop

Primitive operation that introduces a value-bearing event into history.

## Bind

Primitive operation that links existing events and records their relation as a new event.

## Refuse

Primitive operation that records semantic refusal of a target event while preserving full history.

## Collapse

Primitive operation that emits a new representation event derived from one or more targets.

## Frontier

The set of currently active event indices.
Operations may remove events from frontier without deleting history.

## History

Append-only event log containing operations, values, and parent references.

## Continuation

The admissible next-step trajectory of computation represented by possible future history appends.

## Admissibility

Condition describing whether a representation or transition is valid under project semantics.

## Repair

A semantic correction strategy for restoring admissible representation after invalid or refused states.
