from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Event:
    op: str
    value: Any
    parents: tuple[int, ...] = ()


@dataclass
class History:
    events: list[Event] = field(default_factory=list)
    frontier: set[int] = field(default_factory=set)

    def append(self, op: str, value: Any = None, parents: tuple[int, ...] = ()) -> int:
        index = len(self.events)
        self.events.append(Event(op=op, value=value, parents=parents))
        self.frontier.add(index)
        return index

    def pop(self, value: Any) -> int:
        return self.append("POP", value=value)

    def bind(self, left: int, right: int, value: Any = None) -> int:
        self._validate_index(left)
        self._validate_index(right)
        return self.append("BIND", value=value, parents=(left, right))

    def refuse(self, target: int, reason: str | None = None) -> int:
        self._validate_index(target)
        self.frontier.discard(target)
        return self.append("REFUSE", value={"target": target, "reason": reason}, parents=(target,))

    def collapse(self, *targets: int, value: Any = None) -> int:
        if not targets:
            raise ValueError("collapse requires at least one target")
        for target in targets:
            self._validate_index(target)
            self.frontier.discard(target)
        return self.append("COLLAPSE", value=value, parents=tuple(targets))

    def _validate_index(self, index: int) -> None:
        if index < 0 or index >= len(self.events):
            raise IndexError(f"event index out of range: {index}")
