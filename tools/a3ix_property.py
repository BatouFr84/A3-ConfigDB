#!/usr/bin/env python3
"""A3IX property-value index for immutable A3DM snapshots."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping

from tools.a3dm_snapshot import A3DMSnapshot

DEFAULT_PROPERTY_PATHS = ("linkedItems", "weapons", "magazines", "turrets", "transportItems")


@dataclass(frozen=True, order=True)
class A3IXPropertyRef:
    root: str
    classname: str


def _normalize(value: Any) -> tuple[str, Any]:
    if isinstance(value, bool):
        return ("bool", value)
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return ("number", value)
    if isinstance(value, str):
        return ("text", value.casefold())
    raise TypeError(type(value).__name__)


def _scalar_leaves(value: Any):
    if isinstance(value, Mapping):
        for child in value.values():
            yield from _scalar_leaves(child)
    elif isinstance(value, (list, tuple)):
        for child in value:
            yield from _scalar_leaves(child)
    else:
        try:
            yield _normalize(value)
        except TypeError:
            return


class A3IXPropertyIndex:
    """Immutable contains-index over selected resolved properties."""

    def __init__(self, snapshot: A3DMSnapshot, property_paths: tuple[str, ...] = DEFAULT_PROPERTY_PATHS):
        if not property_paths or any(not isinstance(path, str) or not path for path in property_paths):
            raise ValueError("property_paths must contain non-empty strings")
        if len(property_paths) != len(set(property_paths)):
            raise ValueError("property_paths contains duplicates")

        buckets: dict[str, dict[tuple[str, Any], set[A3IXPropertyRef]]] = {path: {} for path in property_paths}
        for root in snapshot.roots:
            for classname, _ in snapshot.iter_classes(root):
                resolved = snapshot.resolved_properties(root, classname)
                ref = A3IXPropertyRef(root, classname)
                for path in property_paths:
                    if path not in resolved:
                        continue
                    for key in _scalar_leaves(resolved[path]):
                        buckets[path].setdefault(key, set()).add(ref)

        self._buckets = MappingProxyType({
            path: MappingProxyType({key: tuple(sorted(refs)) for key, refs in values.items()})
            for path, values in buckets.items()
        })
        self._paths = property_paths
        self._snapshot_id = snapshot.snapshot_id

    @property
    def snapshot_id(self) -> str:
        return self._snapshot_id

    @property
    def property_paths(self) -> tuple[str, ...]:
        return self._paths

    def contains(self, property_path: str, value: Any, *, root: str | None = None) -> tuple[A3IXPropertyRef, ...]:
        if property_path not in self._buckets:
            raise KeyError(f"property path is not indexed: {property_path}")
        try:
            key = _normalize(value)
        except TypeError:
            return ()
        matches = self._buckets[property_path].get(key, ())
        if root is None:
            return matches
        return tuple(ref for ref in matches if ref.root == root)

    def count_keys(self, property_path: str) -> int:
        if property_path not in self._buckets:
            raise KeyError(f"property path is not indexed: {property_path}")
        return len(self._buckets[property_path])
