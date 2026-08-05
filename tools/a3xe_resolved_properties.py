#!/usr/bin/env python3
"""Deterministic local and resolved property computation for A3XE captures."""

from __future__ import annotations

from typing import Any, Mapping

from tools.a3xe_inheritance import build_inheritance_chains


class A3XEResolvedPropertyError(ValueError):
    pass


def _validate_json_value(value: Any, path: str) -> Any:
    if value is None or isinstance(value, (str, bool, int, float)):
        return value
    if isinstance(value, list):
        return [_validate_json_value(item, f"{path}[]") for item in value]
    if isinstance(value, dict):
        validated: dict[str, Any] = {}
        for key in sorted(value):
            if not isinstance(key, str):
                raise A3XEResolvedPropertyError(f"non-string object key at {path}")
            validated[key] = _validate_json_value(value[key], f"{path}.{key}")
        return validated
    raise A3XEResolvedPropertyError(
        f"unsupported property value at {path}: {type(value).__name__}"
    )


def resolve_properties(classes: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    """Return local and resolved properties for every class in deterministic order."""
    chains = build_inheritance_chains(classes)
    output: dict[str, dict[str, Any]] = {}

    for classname in sorted(classes):
        item = classes[classname]
        if not isinstance(item, Mapping):
            raise A3XEResolvedPropertyError(f"class must be an object: {classname}")
        local = item.get("properties", {})
        if not isinstance(local, Mapping):
            raise A3XEResolvedPropertyError(f"properties must be an object: {classname}")

        validated_local = {
            key: _validate_json_value(local[key], f"{classname}.{key}")
            for key in sorted(local)
        }
        resolved: dict[str, Any] = {}
        sources: dict[str, str] = {}
        for ancestor in chains[classname]:
            ancestor_item = classes[ancestor]
            ancestor_properties = ancestor_item.get("properties", {})
            if not isinstance(ancestor_properties, Mapping):
                raise A3XEResolvedPropertyError(
                    f"properties must be an object: {ancestor}"
                )
            for key in sorted(ancestor_properties):
                resolved[key] = _validate_json_value(
                    ancestor_properties[key], f"{ancestor}.{key}"
                )
                sources[key] = ancestor

        output[classname] = {
            "local": validated_local,
            "resolved": resolved,
            "sources": sources,
        }

    return output
