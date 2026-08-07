from __future__ import annotations

from .dictionary import PRIMITIVES
from .lexer import tokenize


def compile_source(source: str) -> list[tuple[str, int | str | None]]:
    bytecode: list[tuple[str, int | str | None]] = []
    for token in tokenize(source):
        if token in PRIMITIVES:
            bytecode.append((token.upper() if token != "." else "DOT", None))
            continue
        try:
            bytecode.append(("PUSH", int(token)))
        except ValueError as exc:
            raise ValueError(f"unknown token: {token}") from exc
    return bytecode
