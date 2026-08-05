#!/usr/bin/env python3
"""A3QM normalized query model for A3-ConfigDB."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping

from tools.a3qe import A3QEFilter, A3QEQuery


class A3QMError(ValueError):
    pass


@dataclass(frozen=True)
class A3QMFilter:
    field: str
    operator: str
    value: Any


@dataclass(frozen=True)
class A3QMQuery:
    root: str | None
    filters: tuple[A3QMFilter, ...]
    limit: int
    offset: int = 0
    sort: str = "classname"
    direction: str = "asc"

    def to_a3qe(self) -> A3QEQuery:
        return A3QEQuery(
            root=self.root,
            filters=tuple(A3QEFilter(item.field, item.operator, item.value) for item in self.filters),
            limit=self.limit,
            offset=self.offset,
            sort=self.sort,
            direction=self.direction,
        )

    def to_dict(self) -> Mapping[str, Any]:
        return MappingProxyType({
            "root": self.root,
            "filters": tuple(MappingProxyType({"field": item.field, "operator": item.operator, "value": item.value}) for item in self.filters),
            "limit": self.limit,
            "offset": self.offset,
            "sort": self.sort,
            "direction": self.direction,
        })


def normalize_query(payload: Mapping[str, Any]) -> A3QMQuery:
    if not isinstance(payload, Mapping):
        raise A3QMError("query payload must be an object")

    unknown = set(payload) - {"root", "filters", "limit", "offset", "sort", "direction"}
    if unknown:
        raise A3QMError(f"unknown query fields: {', '.join(sorted(unknown))}")

    root = payload.get("root")
    if root is not None and (not isinstance(root, str) or not root):
        raise A3QMError("root must be a non-empty string or null")

    limit = payload.get("limit", 100)
    if not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= 500:
        raise A3QMError("limit must be an integer between 1 and 500")
    offset = payload.get("offset", 0)
    if not isinstance(offset, int) or isinstance(offset, bool) or offset < 0:
        raise A3QMError("offset must be a non-negative integer")
    sort = payload.get("sort", "classname")
    if sort not in {"classname", "displayName", "root"}:
        raise A3QMError("sort must be classname, displayName, or root")
    direction = payload.get("direction", "asc")
    if direction not in {"asc", "desc"}:
        raise A3QMError("direction must be asc or desc")

    raw_filters = payload.get("filters", [])
    if not isinstance(raw_filters, (list, tuple)):
        raise A3QMError("filters must be an array")

    filters: list[A3QMFilter] = []
    for index, item in enumerate(raw_filters):
        if not isinstance(item, Mapping):
            raise A3QMError(f"filters[{index}] must be an object")
        unknown_filter = set(item) - {"field", "operator", "value"}
        if unknown_filter:
            raise A3QMError(f"filters[{index}] contains unknown fields: {', '.join(sorted(unknown_filter))}")
        if "value" not in item:
            raise A3QMError(f"filters[{index}].value is required")
        field = item.get("field")
        operator = item.get("operator")
        if not isinstance(field, str) or not field:
            raise A3QMError(f"filters[{index}].field must be a non-empty string")
        if not isinstance(operator, str) or not operator:
            raise A3QMError(f"filters[{index}].operator must be a non-empty string")
        filters.append(A3QMFilter(field=field, operator=operator.casefold(), value=item["value"]))

    return A3QMQuery(root=root, filters=tuple(filters), limit=limit, offset=offset, sort=sort, direction=direction)
