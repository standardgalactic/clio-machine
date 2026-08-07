from __future__ import annotations

import json
import os
from pathlib import Path

from .history import Event, History

DEFAULT_STATE_PATH = ".clio/spherepop_history.json"


def resolve_state_path(path: str | None = None) -> Path:
    candidate = path or os.environ.get("SPHEREPOP_STATE_PATH") or DEFAULT_STATE_PATH
    return Path(candidate)


def load_history(path: str | None = None) -> History:
    state_path = resolve_state_path(path)
    if not state_path.exists():
        return History()
    payload = json.loads(state_path.read_text(encoding="utf-8"))
    events = [Event(op=e["op"], value=e.get("value"), parents=tuple(e.get("parents", ()))) for e in payload["events"]]
    frontier = set(payload.get("frontier", []))
    return History(events=events, frontier=frontier)


def save_history(history: History, path: str | None = None) -> Path:
    state_path = resolve_state_path(path)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "events": [{"op": e.op, "value": e.value, "parents": list(e.parents)} for e in history.events],
        "frontier": sorted(history.frontier),
    }
    state_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return state_path
