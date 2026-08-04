#!/usr/bin/env python3
"""Fail-closed A3DM v0.1 validator and profile reconstructor."""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path
from typing import Any

SUPPORTED_OPS = {"addClass", "removeClass", "setParent", "setProperty"}


class A3DMValidationError(ValueError):
    pass


def _error(message: str) -> None:
    raise A3DMValidationError(message)


def _check_parent_graph(root_name: str, classes: dict[str, Any]) -> None:
    for class_name, class_data in classes.items():
        if not isinstance(class_data, dict):
            _error(f"{root_name}/{class_name}: class must be an object")
        parent = class_data.get("parent")
        if parent is not None and parent not in classes:
            _error(f"{root_name}/{class_name}: missing parent {parent!r}")
        if not isinstance(class_data.get("properties", {}), dict):
            _error(f"{root_name}/{class_name}: properties must be an object")

    for start in classes:
        seen: set[str] = set()
        current: str | None = start
        while current is not None:
            if current in seen:
                _error(f"{root_name}: inheritance cycle involving {current!r}")
            seen.add(current)
            current = classes[current].get("parent")


def _validate_state(roots: dict[str, Any]) -> None:
    if not isinstance(roots, dict):
        _error("roots must be an object")
    for root_name, classes in roots.items():
        if not isinstance(root_name, str) or not root_name:
            _error("root names must be non-empty strings")
        if not isinstance(classes, dict):
            _error(f"{root_name}: root must contain an object of classes")
        _check_parent_graph(root_name, classes)


def _apply_operation(state: dict[str, Any], profile_id: str, index: int, op: dict[str, Any]) -> None:
    if not isinstance(op, dict):
        _error(f"{profile_id} operation {index}: operation must be an object")
    op_name = op.get("op")
    if op_name not in SUPPORTED_OPS:
        _error(f"{profile_id} operation {index}: unsupported operation {op_name!r}")

    root_name = op.get("root")
    class_name = op.get("className")
    if not isinstance(root_name, str) or not isinstance(class_name, str):
        _error(f"{profile_id} operation {index}: root and className are required strings")

    classes = state.setdefault(root_name, {})
    if not isinstance(classes, dict):
        _error(f"{profile_id} operation {index}: root {root_name!r} is invalid")

    if op_name == "addClass":
        if class_name in classes:
            _error(f"{profile_id} operation {index}: class already exists: {class_name}")
        class_data = copy.deepcopy(op.get("class"))
        if not isinstance(class_data, dict):
            _error(f"{profile_id} operation {index}: addClass requires class object")
        class_data.setdefault("parent", None)
        class_data.setdefault("properties", {})
        classes[class_name] = class_data

    elif op_name == "removeClass":
        if class_name not in classes:
            _error(f"{profile_id} operation {index}: missing class: {class_name}")
        dependents = [name for name, data in classes.items() if data.get("parent") == class_name]
        if dependents:
            _error(
                f"{profile_id} operation {index}: cannot remove {class_name}; "
                f"dependent classes: {', '.join(sorted(dependents))}"
            )
        del classes[class_name]

    elif op_name == "setParent":
        if class_name not in classes:
            _error(f"{profile_id} operation {index}: missing class: {class_name}")
        parent = op.get("parent")
        if parent is not None and not isinstance(parent, str):
            _error(f"{profile_id} operation {index}: parent must be string or null")
        classes[class_name]["parent"] = parent

    elif op_name == "setProperty":
        if class_name not in classes:
            _error(f"{profile_id} operation {index}: missing class: {class_name}")
        property_name = op.get("property")
        if not isinstance(property_name, str) or not property_name:
            _error(f"{profile_id} operation {index}: property is required")
        classes[class_name].setdefault("properties", {})[property_name] = copy.deepcopy(op.get("value"))

    try:
        _check_parent_graph(root_name, classes)
    except A3DMValidationError as exc:
        _error(f"{profile_id} operation {index}: {exc}")


def validate_and_reconstruct(package: dict[str, Any]) -> dict[str, dict[str, Any]]:
    if not isinstance(package, dict):
        _error("package must be an object")
    manifest = package.get("manifest")
    profiles = package.get("profiles")
    if not isinstance(manifest, dict) or not isinstance(profiles, dict):
        _error("package requires manifest and profiles objects")
    if manifest.get("format") != "A3DM" or manifest.get("schemaVersion") != "0.1":
        _error("unsupported A3DM format or schemaVersion")

    entries = manifest.get("profiles")
    baseline_id = manifest.get("baselineProfileId")
    if not isinstance(entries, list) or not entries:
        _error("manifest profiles must be a non-empty array")

    entry_map: dict[str, dict[str, Any]] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            _error("manifest profile entries must be objects")
        profile_id = entry.get("profileId")
        if not isinstance(profile_id, str) or not profile_id:
            _error("manifest profileId must be a non-empty string")
        if profile_id in entry_map:
            _error(f"duplicate manifest profileId: {profile_id}")
        entry_map[profile_id] = entry

    if baseline_id not in entry_map or entry_map[baseline_id].get("kind") != "baseline":
        _error("baselineProfileId must reference the baseline entry")
    if set(profiles) != set(entry_map):
        _error("manifest and embedded profile identifiers differ")

    cache: dict[str, dict[str, Any]] = {}
    visiting: set[str] = set()

    def build(profile_id: str) -> dict[str, Any]:
        if profile_id in cache:
            return copy.deepcopy(cache[profile_id])
        if profile_id in visiting:
            _error(f"profile dependency cycle involving {profile_id}")
        if profile_id not in entry_map:
            _error(f"missing profile dependency: {profile_id}")
        visiting.add(profile_id)

        entry = entry_map[profile_id]
        payload = profiles[profile_id]
        if not isinstance(payload, dict) or payload.get("profileId") != profile_id:
            _error(f"{profile_id}: payload identity mismatch")
        if payload.get("kind") != entry.get("kind"):
            _error(f"{profile_id}: payload kind mismatch")

        if entry.get("kind") == "baseline":
            state = copy.deepcopy(payload.get("roots"))
            _validate_state(state)
        elif entry.get("kind") == "delta":
            base_id = entry.get("baseProfileId")
            if payload.get("baseProfileId") != base_id or not isinstance(base_id, str):
                _error(f"{profile_id}: baseProfileId mismatch")
            state = build(base_id)
            operations = payload.get("operations")
            if not isinstance(operations, list):
                _error(f"{profile_id}: operations must be an array")
            for index, operation in enumerate(operations):
                _apply_operation(state, profile_id, index, operation)
            _validate_state(state)
        else:
            _error(f"{profile_id}: unsupported profile kind")

        visiting.remove(profile_id)
        cache[profile_id] = copy.deepcopy(state)
        return copy.deepcopy(state)

    for profile_id in entry_map:
        build(profile_id)
    return cache


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: python tools/a3dm_validator.py <combined-package.json>", file=sys.stderr)
        return 2
    try:
        package = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
        reconstructed = validate_and_reconstruct(package)
    except (OSError, json.JSONDecodeError, A3DMValidationError) as exc:
        print(f"A3DM_VALIDATION=REJECTED\nERROR: {exc}")
        return 1
    print("A3DM_VALIDATION=PASS")
    print("PROFILES=" + ",".join(sorted(reconstructed)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
