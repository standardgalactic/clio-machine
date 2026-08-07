from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class SPEvent:
    eid: int
    op: str
    value: Any = None
    parents: tuple[int, ...] = ()
    frame: int = 0
    active: bool = True


@dataclass
class SPWorld:
    events: list[SPEvent] = field(default_factory=list)
    frontier: set[int] = field(default_factory=set)
    objects: dict[int, str] = field(default_factory=dict)

    def append(
        self,
        op: str,
        *,
        value: Any = None,
        parents: tuple[int, ...] = (),
        frame: int = 0,
        active: bool = True,
    ) -> int:
        eid = len(self.events)
        event = SPEvent(
            eid=eid,
            op=op,
            value=value,
            parents=parents,
            frame=frame,
            active=active,
        )
        self.events.append(event)
        if active:
            self.frontier.add(eid)
        return eid

    def validate(self, eid: int) -> None:
        if eid < 0 or eid >= len(self.events):
            raise IndexError(f"event id out of range: {eid}")

    def register_object(self, eid: int, object_name: str) -> None:
        self.validate(eid)
        self.objects[eid] = object_name

    def active_events(self) -> list[SPEvent]:
        return [self.events[eid] for eid in sorted(self.frontier)]

    def history_until(self, frame: int) -> list[SPEvent]:
        return [event for event in self.events if event.frame <= frame]


def pop(world: SPWorld, value: Any, *, frame: int = 0) -> int:
    return world.append("POP", value=value, frame=frame)


def bind(
    world: SPWorld,
    left: int,
    right: int,
    *,
    value: Any = None,
    frame: int = 0,
) -> int:
    world.validate(left)
    world.validate(right)
    return world.append(
        "BIND",
        value=value,
        parents=(left, right),
        frame=frame,
    )


def refuse(
    world: SPWorld,
    target: int,
    *,
    reason: str | None = None,
    frame: int = 0,
) -> int:
    world.validate(target)
    world.frontier.discard(target)
    return world.append(
        "REFUSE",
        value={"target": target, "reason": reason},
        parents=(target,),
        frame=frame,
        active=False,
    )


def collapse(
    world: SPWorld,
    *targets: int,
    value: Any = None,
    frame: int = 0,
) -> int:
    if not targets:
        raise ValueError("collapse requires at least one target")

    for target in targets:
        world.validate(target)
        world.frontier.discard(target)

    return world.append(
        "COLLAPSE",
        value=value,
        parents=tuple(targets),
        frame=frame,
    )
