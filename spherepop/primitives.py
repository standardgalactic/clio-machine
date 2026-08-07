from __future__ import annotations

from typing import Any

from .history import History


def Pop(history: History, value: Any) -> int:
    return history.pop(value)


def Refuse(history: History, target: int, reason: str | None = None) -> int:
    return history.refuse(target, reason=reason)


def Bind(history: History, left: int, right: int, value: Any = None) -> int:
    return history.bind(left, right, value=value)


def Collapse(history: History, *targets: int, value: Any = None) -> int:
    return history.collapse(*targets, value=value)
