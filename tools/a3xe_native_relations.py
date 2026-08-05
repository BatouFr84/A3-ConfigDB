#!/usr/bin/env python3
"""Derive deterministic native relations from A3DM roots and resolved properties."""

from __future__ import annotations

from typing import Any, Mapping


class A3XENativeRelationError(ValueError):
    pass


RELATION_FIELDS: dict[str, tuple[str, str]] = {
    "weapons": ("CfgWeapons", "many"),
    "magazines": ("CfgMagazines", "many"),
    "ammo": ("CfgAmmo", "one"),
}


def _as_targets(value: Any, mode: str, *, root: str, classname: str, field: str) -> list[str]:
    if mode == "one":
        if value in (None, ""):
            return []
        if not isinstance(value, str):
            raise A3XENativeRelationError(f"{root}/{classname}.{field} must be a string")
        return [value]
    if value is None:
        return []
    if not isinstance(value, (list, tuple)):
        raise A3XENativeRelationError(f"{root}/{classname}.{field} must be an array")
    targets: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item:
            raise A3XENativeRelationError(f"{root}/{classname}.{field} contains an invalid target")
        targets.append(item)
    return sorted(set(targets))


def build_native_relations(
    roots: Mapping[str, Mapping[str, Mapping[str, Any]]],
    resolved_by_root: Mapping[str, Mapping[str, Mapping[str, Any]]],
) -> dict[str, Any]:
    """Build parent/children and known outbound relations for every class."""
    relations: dict[str, Any] = {}
    missing: list[dict[str, str]] = []

    for root in sorted(roots):
        classes = roots[root]
        resolved_classes = resolved_by_root.get(root, {})
        root_relations: dict[str, Any] = {}
        children: dict[str, list[str]] = {name: [] for name in classes}

        for classname, class_data in classes.items():
            parent = class_data.get("parent")
            if parent is not None:
                if not isinstance(parent, str) or not parent:
                    raise A3XENativeRelationError(f"invalid parent: {root}/{classname}")
                if parent not in classes:
                    raise A3XENativeRelationError(f"missing parent: {root}/{classname} -> {parent}")
                children[parent].append(classname)

        for classname in sorted(classes):
            class_data = classes[classname]
            resolved_entry = resolved_classes.get(classname, {})
            resolved = resolved_entry.get("resolved", {})
            sources = resolved_entry.get("sources", {})
            if not isinstance(resolved, Mapping) or not isinstance(sources, Mapping):
                raise A3XENativeRelationError(f"missing resolved properties: {root}/{classname}")

            outbound: dict[str, list[dict[str, Any]]] = {}
            for field, (target_root, mode) in RELATION_FIELDS.items():
                if field not in resolved:
                    continue
                targets = _as_targets(resolved[field], mode, root=root, classname=classname, field=field)
                entries: list[dict[str, Any]] = []
                for target in targets:
                    exists = target_root in roots and target in roots[target_root]
                    entry = {
                        "root": target_root,
                        "classname": target,
                        "exists": exists,
                        "sourceClass": sources.get(field),
                    }
                    entries.append(entry)
                    if not exists:
                        missing.append({
                            "sourceRoot": root,
                            "sourceClass": classname,
                            "field": field,
                            "targetRoot": target_root,
                            "targetClass": target,
                        })
                outbound[field] = entries

            root_relations[classname] = {
                "parent": class_data.get("parent"),
                "children": sorted(children[classname]),
                "outbound": outbound,
            }
        relations[root] = root_relations

    missing.sort(key=lambda item: (
        item["sourceRoot"], item["sourceClass"], item["field"],
        item["targetRoot"], item["targetClass"],
    ))
    return {
        "complete": not missing,
        "roots": relations,
        "missingTargets": missing,
    }
