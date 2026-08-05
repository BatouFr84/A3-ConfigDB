#!/usr/bin/env python3
"""A3QE v0.1 query engine over immutable A3DM snapshots and A3IX indexes."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from tools.a3dm_snapshot import A3DMSnapshot
from tools.a3ix_exact import A3IXExactIndex
from tools.a3ix_property import A3IXPropertyIndex


class A3QEQueryError(ValueError):
    pass


@dataclass(frozen=True)
class A3QEFilter:
    field: str
    operator: str
    value: Any


@dataclass(frozen=True)
class A3QEQuery:
    root: str | None = None
    filters: tuple[A3QEFilter, ...] = ()
    limit: int = 100


@dataclass(frozen=True, order=True)
class A3QEResult:
    root: str
    classname: str


class A3QEEngine:
    """Deterministic AND query executor using A3IX indexes only."""

    def __init__(self, snapshot: A3DMSnapshot):
        self._snapshot = snapshot
        self._exact = A3IXExactIndex(snapshot)
        self._property = A3IXPropertyIndex(snapshot)

    @property
    def snapshot_id(self) -> str:
        return self._snapshot.snapshot_id

    def execute(self, query: A3QEQuery) -> tuple[A3QEResult, ...]:
        self._validate_query(query)

        candidate_sets: list[set[A3QEResult]] = []
        if query.root is not None:
            candidate_sets.append({
                A3QEResult(ref.root, ref.classname)
                for ref in self._exact.exact("root", query.root)
            })

        for condition in query.filters:
            candidate_sets.append(self._execute_filter(condition, query.root))

        if candidate_sets:
            matches = set.intersection(*candidate_sets)
        else:
            matches = {
                A3QEResult(root, classname)
                for root in self._snapshot.roots
                for classname in self._snapshot.class_names(root)
            }

        return tuple(sorted(matches))[: query.limit]

    def _execute_filter(self, condition: A3QEFilter, root: str | None) -> set[A3QEResult]:
        operator = condition.operator.casefold()

        if operator == "eq":
            try:
                refs = self._exact.exact(condition.field, condition.value, root=root)
            except KeyError as exc:
                raise A3QEQueryError(str(exc)) from exc
            return {A3QEResult(ref.root, ref.classname) for ref in refs}

        if operator == "contains":
            try:
                refs = self._property.contains(condition.field, condition.value, root=root)
            except KeyError as exc:
                raise A3QEQueryError(str(exc)) from exc
            return {A3QEResult(ref.root, ref.classname) for ref in refs}

        raise A3QEQueryError(f"unsupported operator: {condition.operator}")

    def _validate_query(self, query: A3QEQuery) -> None:
        if not isinstance(query, A3QEQuery):
            raise A3QEQueryError("query must be an A3QEQuery")
        if query.root is not None and not self._snapshot.has_root(query.root):
            raise A3QEQueryError(f"unknown root: {query.root}")
        if not isinstance(query.limit, int) or isinstance(query.limit, bool) or not 1 <= query.limit <= 500:
            raise A3QEQueryError("limit must be an integer between 1 and 500")
        if not isinstance(query.filters, tuple):
            raise A3QEQueryError("filters must be a tuple")
        for index, condition in enumerate(query.filters):
            if not isinstance(condition, A3QEFilter):
                raise A3QEQueryError(f"filters[{index}] must be an A3QEFilter")
            if not isinstance(condition.field, str) or not condition.field:
                raise A3QEQueryError(f"filters[{index}].field must be a non-empty string")
            if not isinstance(condition.operator, str) or not condition.operator:
                raise A3QEQueryError(f"filters[{index}].operator must be a non-empty string")
