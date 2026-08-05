#!/usr/bin/env python3
"""Deterministic hybrid query planning for A3QE."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Iterable


@dataclass(frozen=True)
class A3QEPlanStep:
    field: str
    operator: str
    index: str
    estimated_matches: int
    ordinal: int


@dataclass(frozen=True)
class A3QEPlan:
    root: str | None
    steps: tuple[A3QEPlanStep, ...]
    complete: bool = True
    fallback: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "root": self.root,
            "complete": self.complete,
            "fallback": self.fallback,
            "steps": [
                {
                    "field": step.field,
                    "operator": step.operator,
                    "index": step.index,
                    "estimatedMatches": step.estimated_matches,
                    "ordinal": step.ordinal,
                }
                for step in self.steps
            ],
        }


class A3QEPlanner:
    """Classify filters and order them by deterministic selectivity estimates."""

    def __init__(self, *, text_fields: Iterable[str], property_fields: Iterable[str]):
        self._text_fields = frozenset(text_fields)
        self._property_fields = frozenset(property_fields)

    def index_for(self, field: str, operator: str) -> str:
        normalized = operator.casefold()
        if normalized == "eq":
            return "exact"
        if normalized == "contains" and field in self._text_fields:
            return "text"
        if normalized == "contains" and field in self._property_fields:
            return "property"
        raise ValueError(f"no complete index route for {field} {operator}")

    def plan(
        self,
        query: Any,
        estimate: Callable[[Any, str], int],
    ) -> A3QEPlan:
        steps = []
        if query.root is not None:
            steps.append(A3QEPlanStep("root", "eq", "exact", estimate(None, "root"), -1))
        for ordinal, condition in enumerate(query.filters):
            index = self.index_for(condition.field, condition.operator)
            steps.append(A3QEPlanStep(
                condition.field,
                condition.operator.casefold(),
                index,
                estimate(condition, index),
                ordinal,
            ))
        ordered = tuple(sorted(
            steps,
            key=lambda step: (step.estimated_matches, step.index, step.field, step.ordinal),
        ))
        return A3QEPlan(root=query.root, steps=ordered)
