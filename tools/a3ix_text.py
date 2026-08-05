#!/usr/bin/env python3
"""A3IX v0.1 case-insensitive substring text index."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from tools.a3dm_snapshot import A3DMSnapshot

TEXT_INDEXED_FIELDS = (
    "classname",
    "displayName",
    "author",
    "faction",
    "dlc",
)


@dataclass(frozen=True, order=True)
class A3IXTextRef:
    root: str
    classname: str


class A3IXTextIndex:
    """Immutable text-value index supporting deterministic substring search."""

    def __init__(self, snapshot: A3DMSnapshot):
        values: dict[str, list[tuple[str, A3IXTextRef]]] = {
            field: [] for field in TEXT_INDEXED_FIELDS
        }
        for root in snapshot.roots:
            for classname, _class_data in snapshot.iter_classes(root):
                resolved = snapshot.resolved_properties(root, classname)
                ref = A3IXTextRef(root, classname)
                source = {
                    "classname": classname,
                    "displayName": resolved.get("displayName"),
                    "author": resolved.get("author"),
                    "faction": resolved.get("faction"),
                    "dlc": resolved.get("dlc"),
                }
                for field, value in source.items():
                    if isinstance(value, str):
                        values[field].append((value.casefold(), ref))

        self._values: Mapping[str, tuple[tuple[str, A3IXTextRef], ...]] = MappingProxyType({
            field: tuple(sorted(entries, key=lambda item: (item[1], item[0])))
            for field, entries in values.items()
        })
        self._snapshot_id = snapshot.snapshot_id

    @property
    def snapshot_id(self) -> str:
        return self._snapshot_id

    @property
    def fields(self) -> tuple[str, ...]:
        return TEXT_INDEXED_FIELDS

    def contains(self, field: str, value: str, *, root: str | None = None) -> tuple[A3IXTextRef, ...]:
        if field not in self._values:
            raise KeyError(f"field is not text indexed: {field}")
        if not isinstance(value, str):
            return ()
        needle = value.casefold()
        if not needle:
            return ()
        matches = {
            ref for text, ref in self._values[field]
            if needle in text and (root is None or ref.root == root)
        }
        return tuple(sorted(matches))
