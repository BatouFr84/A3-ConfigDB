#!/usr/bin/env python3
"""A3IX v0.1 exact-match index for immutable A3DM snapshots."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Iterable, Mapping

from tools.a3dm_snapshot import A3DMSnapshot

INDEXED_FIELDS = (
    "classname",
    "root",
    "displayName",
    "parent",
    "scope",
    "author",
    "dlc",
    "faction",
)


@dataclass(frozen=True, order=True)
class A3IXAssetRef:
    root: str
    classname: str


def _normalize(value: Any) -> tuple[str, Any]:
    if isinstance(value, bool):
        return ("bool", value)
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return ("number", value)
    if isinstance(value, str):
        return ("text", value.casefold())
    raise TypeError(f"unsupported exact-index value: {type(value).__name__}")


class A3IXExactIndex:
    """Immutable exact-match index over one validated snapshot."""

    def __init__(self, snapshot: A3DMSnapshot):
        buckets: dict[str, dict[tuple[str, Any], set[A3IXAssetRef]]] = {
            field: {} for field in INDEXED_FIELDS
        }

        for root in snapshot.roots:
            for classname, class_data in snapshot.iter_classes(root):
                ref = A3IXAssetRef(root=root, classname=classname)
                resolved = snapshot.resolved_properties(root, classname)
                values = {
                    "classname": classname,
                    "root": root,
                    "displayName": resolved.get("displayName"),
                    "parent": class_data.get("parent"),
                    "scope": resolved.get("scope"),
                    "author": resolved.get("author"),
                    "dlc": resolved.get("dlc"),
                    "faction": resolved.get("faction"),
                }
                for field, value in values.items():
                    if value is None:
                        continue
                    try:
                        key = _normalize(value)
                    except TypeError:
                        continue
                    buckets[field].setdefault(key, set()).add(ref)

        frozen: dict[str, Mapping[tuple[str, Any], tuple[A3IXAssetRef, ...]]] = {}
        for field, values in buckets.items():
            frozen[field] = MappingProxyType(
                {key: tuple(sorted(refs)) for key, refs in values.items()}
            )
        self._buckets = MappingProxyType(frozen)
        self._snapshot_id = snapshot.snapshot_id

    @property
    def snapshot_id(self) -> str:
        return self._snapshot_id

    @property
    def fields(self) -> tuple[str, ...]:
        return INDEXED_FIELDS

    def exact(self, field: str, value: Any, *, root: str | None = None) -> tuple[A3IXAssetRef, ...]:
        if field not in self._buckets:
            raise KeyError(f"field is not indexed: {field}")
        try:
            key = _normalize(value)
        except TypeError:
            return ()
        matches = self._buckets[field].get(key, ())
        if root is None:
            return matches
        return tuple(ref for ref in matches if ref.root == root)

    def contains_ref(self, field: str, value: Any, ref: A3IXAssetRef) -> bool:
        return ref in self.exact(field, value)

    def count_keys(self, field: str) -> int:
        if field not in self._buckets:
            raise KeyError(f"field is not indexed: {field}")
        return len(self._buckets[field])
