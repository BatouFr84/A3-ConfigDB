#!/usr/bin/env python3
"""Fail-closed validator for A3DM v0.1 snapshot packages."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


class A3DMValidationError(ValueError):
    pass


def _error(message: str) -> None:
    raise A3DMValidationError(message)


def _require_non_empty_string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value:
        _error(f"{field} must be a non-empty string")
    return value


def _validate_addons(addons: Any) -> None:
    if not isinstance(addons, list):
        _error("manifest.loadedAddons must be an array")

    seen_orders: set[int] = set()
    seen_ids: set[str] = set()
    expected_order = 0

    for index, addon in enumerate(addons):
        if not isinstance(addon, dict):
            _error(f"manifest.loadedAddons[{index}] must be an object")
        order = addon.get("order")
        addon_id = _require_non_empty_string(addon.get("id"), f"manifest.loadedAddons[{index}].id")
        _require_non_empty_string(addon.get("name"), f"manifest.loadedAddons[{index}].name")
        if not isinstance(order, int) or order < 0:
            _error(f"manifest.loadedAddons[{index}].order must be a non-negative integer")
        if order in seen_orders:
            _error(f"duplicate addon order: {order}")
        if addon_id in seen_ids:
            _error(f"duplicate addon id: {addon_id}")
        if order != expected_order:
            _error(
                "manifest.loadedAddons order must be contiguous and match array order: "
                f"expected {expected_order}, got {order}"
            )
        seen_orders.add(order)
        seen_ids.add(addon_id)
        expected_order += 1


def _validate_parent_graph(root_name: str, classes: Any) -> None:
    if not isinstance(classes, dict):
        _error(f"snapshot.roots.{root_name} must be an object")

    for class_name, class_data in classes.items():
        if not isinstance(class_name, str) or not class_name:
            _error(f"snapshot.roots.{root_name} contains an invalid class name")
        if not isinstance(class_data, dict):
            _error(f"{root_name}/{class_name}: class must be an object")
        parent = class_data.get("parent")
        if parent is not None and not isinstance(parent, str):
            _error(f"{root_name}/{class_name}: parent must be string or null")
        if parent is not None and parent not in classes:
            _error(f"{root_name}/{class_name}: missing parent {parent!r}")
        if not isinstance(class_data.get("properties"), dict):
            _error(f"{root_name}/{class_name}: properties must be an object")

    for start in classes:
        seen: set[str] = set()
        current: str | None = start
        while current is not None:
            if current in seen:
                _error(f"{root_name}: inheritance cycle involving {current!r}")
            seen.add(current)
            current = classes[current].get("parent")


def validate_snapshot_package(package: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(package, dict):
        _error("package must be an object")

    manifest = package.get("manifest")
    snapshot = package.get("snapshot")
    if not isinstance(manifest, dict) or not isinstance(snapshot, dict):
        _error("package requires manifest and snapshot objects")

    if manifest.get("format") != "A3DM":
        _error("unsupported package format")
    if manifest.get("schemaVersion") != "0.1":
        _error("unsupported A3DM schemaVersion")

    required_strings = (
        "packageVersion",
        "datasetId",
        "snapshotId",
        "createdAt",
        "extractorVersion",
        "gameVersion",
        "presetLabel",
    )
    for field in required_strings:
        _require_non_empty_string(manifest.get(field), f"manifest.{field}")

    if not isinstance(manifest.get("artificialDataOnly"), bool):
        _error("manifest.artificialDataOnly must be boolean")
    if not isinstance(manifest.get("sourceGameDataIncluded"), bool):
        _error("manifest.sourceGameDataIncluded must be boolean")
    if manifest.get("artificialDataOnly") and manifest.get("sourceGameDataIncluded"):
        _error("artificialDataOnly=true conflicts with sourceGameDataIncluded=true")

    active_dlc = manifest.get("activeDlc")
    if not isinstance(active_dlc, list) or any(not isinstance(item, str) or not item for item in active_dlc):
        _error("manifest.activeDlc must be an array of non-empty strings")
    if len(active_dlc) != len(set(active_dlc)):
        _error("manifest.activeDlc contains duplicates")

    _validate_addons(manifest.get("loadedAddons"))

    snapshot_id = _require_non_empty_string(snapshot.get("snapshotId"), "snapshot.snapshotId")
    if snapshot_id != manifest.get("snapshotId"):
        _error("manifest.snapshotId and snapshot.snapshotId differ")

    roots = snapshot.get("roots")
    if not isinstance(roots, dict) or not roots:
        _error("snapshot.roots must be a non-empty object")

    for root_name, classes in roots.items():
        if not isinstance(root_name, str) or not root_name:
            _error("snapshot root names must be non-empty strings")
        _validate_parent_graph(root_name, classes)

    return snapshot


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: python tools/a3dm_validator.py <snapshot-package.json>", file=sys.stderr)
        return 2

    try:
        package = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
        snapshot = validate_snapshot_package(package)
    except (OSError, json.JSONDecodeError, A3DMValidationError) as exc:
        print(f"A3DM_VALIDATION=REJECTED\nERROR: {exc}")
        return 1

    class_count = sum(len(classes) for classes in snapshot["roots"].values())
    print("A3DM_VALIDATION=PASS")
    print(f"SNAPSHOT={snapshot['snapshotId']}")
    print(f"ROOTS={len(snapshot['roots'])}")
    print(f"CLASSES={class_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
