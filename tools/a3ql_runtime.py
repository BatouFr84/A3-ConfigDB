#!/usr/bin/env python3
"""Execute A3QL source text through A3QM and A3QE."""

from __future__ import annotations

from dataclasses import dataclass

from tools.a3dm_snapshot import A3DMSnapshot
from tools.a3ql import A3QLSyntaxError, parse_a3ql
from tools.a3qe import A3QEEngine, A3QEQueryError, A3QEResult


class A3QLExecutionError(ValueError):
    """Raised when a syntactically valid query cannot be executed."""


@dataclass(frozen=True)
class A3QLExecution:
    source: str
    snapshot_id: str
    results: tuple[A3QEResult, ...]


class A3QLRuntime:
    """Single public entry point for parsing and executing A3QL."""

    def __init__(self, snapshot: A3DMSnapshot):
        self._engine = A3QEEngine(snapshot)

    @property
    def snapshot_id(self) -> str:
        return self._engine.snapshot_id

    def execute(self, source: str) -> A3QLExecution:
        try:
            normalized = parse_a3ql(source)
            results = self._engine.execute(normalized.to_a3qe())
        except A3QLSyntaxError:
            raise
        except A3QEQueryError as exc:
            raise A3QLExecutionError(str(exc)) from exc
        return A3QLExecution(source=source, snapshot_id=self.snapshot_id, results=results)


def execute_a3ql(snapshot: A3DMSnapshot, source: str) -> tuple[A3QEResult, ...]:
    """Convenience helper returning only the deterministic result tuple."""
    return A3QLRuntime(snapshot).execute(source).results
