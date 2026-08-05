#!/usr/bin/env python3
"""A3QL v0.1 parser producing the normalized A3QM query model."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from tools.a3qm import A3QMError, A3QMQuery, normalize_query


class A3QLSyntaxError(ValueError):
    pass


_TOKEN_RE = re.compile(
    r'''\s*(?:(?P<string>"(?:\\.|[^"\\])*")|(?P<number>-?(?:\d+\.\d+|\d+))|(?P<word>[A-Za-z_][A-Za-z0-9_]*))'''
)


@dataclass(frozen=True)
class _Token:
    kind: str
    text: str
    position: int


def _tokenize(source: str) -> tuple[_Token, ...]:
    tokens: list[_Token] = []
    position = 0
    while position < len(source):
        match = _TOKEN_RE.match(source, position)
        if not match:
            if source[position:].strip() == "":
                break
            raise A3QLSyntaxError(f"unexpected character at position {position}")
        kind = match.lastgroup
        assert kind is not None
        tokens.append(_Token(kind, match.group(kind), match.start(kind)))
        position = match.end()
    return tuple(tokens)


def _decode_value(token: _Token) -> Any:
    if token.kind == "string":
        try:
            return bytes(token.text[1:-1], "utf-8").decode("unicode_escape")
        except UnicodeDecodeError as exc:
            raise A3QLSyntaxError(f"invalid string escape at position {token.position}") from exc
    if token.kind == "number":
        return float(token.text) if "." in token.text else int(token.text)
    if token.kind == "word":
        lowered = token.text.casefold()
        if lowered == "true":
            return True
        if lowered == "false":
            return False
    raise A3QLSyntaxError(f"expected value at position {token.position}")


def parse_a3ql(source: str) -> A3QMQuery:
    if not isinstance(source, str) or not source.strip():
        raise A3QLSyntaxError("query must be a non-empty string")

    tokens = _tokenize(source)
    cursor = 0

    def peek() -> _Token | None:
        return tokens[cursor] if cursor < len(tokens) else None

    def consume_word(expected: str | None = None) -> _Token:
        nonlocal cursor
        token = peek()
        if token is None or token.kind != "word":
            position = len(source) if token is None else token.position
            label = expected or "identifier"
            raise A3QLSyntaxError(f"expected {label} at position {position}")
        if expected is not None and token.text.casefold() != expected.casefold():
            raise A3QLSyntaxError(f"expected {expected} at position {token.position}")
        cursor += 1
        return token

    consume_word("FROM")
    root = consume_word().text

    filters: list[dict[str, Any]] = []
    token = peek()
    if token is not None and token.kind == "word" and token.text.casefold() == "where":
        consume_word("WHERE")
        while True:
            field = consume_word().text
            operator_token = consume_word()
            operator = operator_token.text.casefold()
            if operator not in {"eq", "contains"}:
                raise A3QLSyntaxError(
                    f"unsupported operator {operator_token.text!r} at position {operator_token.position}"
                )
            value_token = peek()
            if value_token is None:
                raise A3QLSyntaxError(f"expected value at position {len(source)}")
            if value_token.kind not in {"string", "number", "word"}:
                raise A3QLSyntaxError(f"expected value at position {value_token.position}")
            cursor += 1
            filters.append({"field": field, "operator": operator, "value": _decode_value(value_token)})

            token = peek()
            if token is not None and token.kind == "word" and token.text.casefold() == "and":
                consume_word("AND")
                continue
            break

    limit = 100
    token = peek()
    if token is not None and token.kind == "word" and token.text.casefold() == "limit":
        consume_word("LIMIT")
        value_token = peek()
        if value_token is None or value_token.kind != "number" or "." in value_token.text:
            position = len(source) if value_token is None else value_token.position
            raise A3QLSyntaxError(f"LIMIT requires an integer at position {position}")
        cursor += 1
        limit = int(value_token.text)

    if cursor != len(tokens):
        token = tokens[cursor]
        raise A3QLSyntaxError(f"unexpected token {token.text!r} at position {token.position}")

    try:
        return normalize_query({"root": root, "filters": filters, "limit": limit})
    except A3QMError as exc:
        raise A3QLSyntaxError(str(exc)) from exc
