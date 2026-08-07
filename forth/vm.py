from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from spherepop.history import History
from spherepop.primitives import Bind, Collapse, Pop, Refuse


@dataclass
class ForthVM:
    history: History = field(default_factory=History)
    stack: list[int] = field(default_factory=list)
    values: dict[int, int] = field(default_factory=dict)
    output: list[int] = field(default_factory=list)

    def execute(self, bytecode: list[tuple[str, int | str | None]]) -> list[int]:
        for op, arg in bytecode:
            if op == "PUSH":
                index = Pop(self.history, arg)
                self.stack.append(index)
                self.values[index] = int(arg)
            elif op in {"+", "-", "*", "/"}:
                self._binary(op)
            elif op == "DOT":
                self._dot()
            else:
                raise ValueError(f"unknown op: {op}")
        return self.output

    def _binary(self, op: str) -> None:
        right = self.stack.pop()
        left = self.stack.pop()
        left_value = self.values[left]
        right_value = self.values[right]
        operator = _binary_operator(op)
        result = operator(left_value, right_value)

        relation = Bind(self.history, left, right, value={"op": op})
        result_index = Collapse(self.history, relation, left, right, value=result)
        self.values[result_index] = result
        self.stack.append(result_index)

    def _dot(self) -> None:
        target = self.stack.pop()
        self.output.append(self.values[target])
        Refuse(self.history, target, reason="printed")
        Collapse(self.history, target, value="drop")


def _binary_operator(op: str) -> Callable[[int, int], int]:
    if op == "+":
        return lambda left, right: left + right
    if op == "-":
        return lambda left, right: left - right
    if op == "*":
        return lambda left, right: left * right
    if op == "/":
        return lambda left, right: left // right
    raise ValueError(f"unsupported op: {op}")
