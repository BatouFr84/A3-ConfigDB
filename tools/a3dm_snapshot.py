#!/usr/bin/env python3
"""Immutable A3DM snapshot loading and access API."""

from __future__ import annotations

import json
from pathlib import Path
from types import MappingProxyType
from typing import Any, Iterator, Mapping

from tools.a3dm_validator import A3DMValidationError, validate_snapshot_package


class A3DMSnapshotError(ValueError):
    pass


def _freeze(value: Any) -> Any:
    if isinstance(value, dict):
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_freeze(item) for item in value)
    return value


class A3DMSnapshot:
    """Read-only view over one validated A3DM snapshot package."""

    def __init__(self, package: Mapping[str, Any]):
        mutable_package = dict(package)
        try:
            validated_snapshot = validate_snapshot_package(mutable_package)
        except A3DMValidationError as exc:
            raise A3DMSnapshotError(str(exc)) from exc

        self._manifest = _freeze(mutable_package["manifest"])
        self._snapshot = _freeze(validated_snapshot)
        self._roots = self._snapshot["roots"]

    @classmethod
    def from_file(cls, path: str | Path) -> "A3DMSnapshot":
        source = Path(path)
        try:
            package = json.loads(source.read_text(encoding="utf-8"))
        except OSError as exc:
            raise A3DMSnapshotError(f"cannot read snapshot: {exc}") from exc
        except json.JSONDecodeError as exc:
            raise A3DMSnapshotError(f"invalid JSON: {exc}") from exc
        return cls(package)

    @property
    def manifest(self) -> Mapping[str, Any]:
        return self._manifest

    @property
    def snapshot_id(self) -> str:
        return self._snapshot["snapshotId"]

    @property
    def game_version(self) -> str:
        return self._manifest["gameVersion"]

    @property
    def preset_label(self) -> str:
        return self._manifest["presetLabel"]

    @property
    def roots(self) -> tuple[str, ...]:
        return tuple(sorted(self._roots))

    def has_root(self, root: str) -> bool:
        return root in self._roots

    def class_names(self, root: str) -> tuple[str, ...]:
        classes = self._get_root(root)
        return tuple(sorted(classes))

    def iter_classes(self, root: str) -> Iterator[tuple[str, Mapping[str, Any]]]:
        classes = self._get_root(root)
        for class_name in sorted(classes):
            yield class_name, classes[class_name]

    def get_class(self, root: str, class_name: str) -> Mapping[str, Any]:
        classes = self._get_root(root)
        try:
            return classes[class_name]
        except KeyError as exc:
            raise A3DMSnapshotError(f"unknown class: {root}/{class_name}") from exc

    def resolved_properties(self, root: str, class_name: str) -> Mapping[str, Any]:
        classes = self._get_root(root)
        if class_name not in classes:
            raise A3DMSnapshotError(f"unknown class: {root}/{class_name}")

        chain: list[Mapping[str, Any]] = []
        current: str | None = class_name
        while current is not None:
            class_data = classes[current]
            chain.append(class_data)
            current = class_data.get("parent")

        merged: dict[str, Any] = {}
        for class_data in reversed(chain):
            merged.update(class_data.get("properties", {}))
        return _freeze(merged)

    def _get_root(self, root: str) -> Mapping[str, Any]:
        try:
            return self._roots[root]
        except KeyError as exc:
            raise A3DMSnapshotError(f"unknown root: {root}") from exc
