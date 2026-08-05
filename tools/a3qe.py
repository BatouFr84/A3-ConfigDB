#!/usr/bin/env python3
"""A3QE query engine over immutable A3DM snapshots and A3IX indexes."""

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
from typing import Any

from tools.a3dm_snapshot import A3DMSnapshot
from tools.a3ix_exact import A3IXExactIndex
from tools.a3ix_property import A3IXPropertyIndex
from tools.a3ix_text import A3IXTextIndex
from tools.a3qe_planner import A3QEPlan, A3QEPlanner


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
    offset: int = 0
    sort: str = "root"
    direction: str = "asc"


@dataclass(frozen=True, order=True)
class A3QEResult:
    root: str
    classname: str


@dataclass(frozen=True)
class A3QEExecution:
    results: tuple[A3QEResult, ...]
    total: int
    offset: int
    limit: int
    sort: str
    direction: str
    duration_ms: float
    plan: A3QEPlan


class A3QEEngine:
    """Deterministic AND executor with complete indexed plans."""

    def __init__(self, snapshot: A3DMSnapshot):
        self._snapshot = snapshot
        self._exact = A3IXExactIndex(snapshot)
        self._property = A3IXPropertyIndex(snapshot)
        self._text = A3IXTextIndex(snapshot)
        self._planner = A3QEPlanner(text_fields=self._text.fields, property_fields=self._property.property_paths)
        self._last_plan: A3QEPlan | None = None

    @property
    def snapshot_id(self) -> str:
        return self._snapshot.snapshot_id

    @property
    def text_indexed_fields(self) -> tuple[str, ...]:
        return self._text.fields

    @property
    def last_plan(self) -> A3QEPlan | None:
        return self._last_plan

    def explain(self, query: A3QEQuery) -> A3QEPlan:
        self._validate_query(query)
        try:
            return self._planner.plan(query, lambda condition, index: self._estimate(query, condition, index))
        except (KeyError, ValueError) as exc:
            raise A3QEQueryError(str(exc)) from exc

    def execute(self, query: A3QEQuery) -> tuple[A3QEResult, ...]:
        return self.execute_page(query).results

    def execute_page(self, query: A3QEQuery) -> A3QEExecution:
        started = perf_counter()
        plan = self.explain(query)
        self._last_plan = plan
        conditions = {ordinal: condition for ordinal, condition in enumerate(query.filters)}
        matches: set[A3QEResult] | None = None

        for step in plan.steps:
            refs = self._exact.exact("root", query.root) if step.ordinal == -1 else self._refs_for(conditions[step.ordinal], query.root, step.index)
            current = {A3QEResult(ref.root, ref.classname) for ref in refs}
            matches = current if matches is None else matches.intersection(current)
            if not matches:
                break

        if matches is None:
            matches = {A3QEResult(root, classname) for root in self._snapshot.roots for classname in self._snapshot.class_names(root)}

        ordered = sorted(matches, key=lambda item: self._sort_key(item, query.sort), reverse=query.direction == "desc")
        total = len(ordered)
        page = tuple(ordered[query.offset: query.offset + query.limit])
        return A3QEExecution(page, total, query.offset, query.limit, query.sort, query.direction, round((perf_counter() - started) * 1000, 3), plan)

    def _sort_key(self, item: A3QEResult, field: str):
        if field == "root":
            return (item.root.casefold(), item.classname.casefold())
        if field == "displayName":
            display = self._snapshot.resolved_properties(item.root, item.classname).get("displayName")
            return (str(display or "").casefold(), item.root.casefold(), item.classname.casefold())
        return (item.classname.casefold(), item.root.casefold())

    def _estimate(self, query: A3QEQuery, condition: A3QEFilter | None, index: str) -> int:
        if condition is None:
            return len(self._exact.exact("root", query.root))
        return len(self._refs_for(condition, query.root, index))

    def _refs_for(self, condition: A3QEFilter, root: str | None, index: str):
        try:
            if index == "exact":
                return self._exact.exact(condition.field, condition.value, root=root)
            if index == "text":
                return self._text.contains(condition.field, condition.value, root=root)
            if index == "property":
                return self._property.contains(condition.field, condition.value, root=root)
        except KeyError as exc:
            raise A3QEQueryError(str(exc)) from exc
        raise A3QEQueryError(f"unsupported index route: {index}")

    def _validate_query(self, query: A3QEQuery) -> None:
        if not isinstance(query, A3QEQuery):
            raise A3QEQueryError("query must be an A3QEQuery")
        if query.root is not None and not self._snapshot.has_root(query.root):
            raise A3QEQueryError(f"unknown root: {query.root}")
        if not isinstance(query.limit, int) or isinstance(query.limit, bool) or not 1 <= query.limit <= 500:
            raise A3QEQueryError("limit must be an integer between 1 and 500")
        if not isinstance(query.offset, int) or isinstance(query.offset, bool) or query.offset < 0:
            raise A3QEQueryError("offset must be a non-negative integer")
        if query.sort not in {"classname", "displayName", "root"}:
            raise A3QEQueryError("sort must be classname, displayName, or root")
        if query.direction not in {"asc", "desc"}:
            raise A3QEQueryError("direction must be asc or desc")
        if not isinstance(query.filters, tuple):
            raise A3QEQueryError("filters must be a tuple")
        for index, condition in enumerate(query.filters):
            if not isinstance(condition, A3QEFilter):
                raise A3QEQueryError(f"filters[{index}] must be an A3QEFilter")
            if not isinstance(condition.field, str) or not condition.field:
                raise A3QEQueryError(f"filters[{index}].field must be a non-empty string")
            if not isinstance(condition.operator, str) or not condition.operator:
                raise A3QEQueryError(f"filters[{index}].operator must be a non-empty string")
