from __future__ import annotations

import json
from typing import Iterable

from .history import History


def render_trace(history: History) -> str:
    lines = []
    active = sorted(history.frontier)
    lines.append(f"frontier={active}")
    for i, event in enumerate(history.events):
        lines.append(f"{i:04d} {event.op:<8} parents={list(event.parents)} value={event.value!r}")
    return "\n".join(lines)


def events_as_jsonl(history: History) -> Iterable[str]:
    for i, event in enumerate(history.events, start=1):
        yield json.dumps({"t": i, "op": event.op, "value": event.value, "parents": list(event.parents)}, sort_keys=True)
