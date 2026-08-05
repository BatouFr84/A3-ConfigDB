#!/usr/bin/env python3
"""Typed relation resolver for one immutable A3DM snapshot."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping

from tools.a3dm_snapshot import A3DMSnapshot


RELATION_TARGET_ROOTS: Mapping[str, str] = {
    "weapons": "CfgWeapons",
    "magazines": "CfgMagazines",
    "ammo": "CfgAmmo",
}


@dataclass(frozen=True, order=True)
class A3RelationTarget:
    root: str
    classname: str
    exists: bool

    def to_dict(self) -> dict[str, Any]:
        return {"root": self.root, "classname": self.classname, "exists": self.exists}


class A3RelationResolver:
    """Resolve inheritance and selected classname-bearing properties."""

    def __init__(self, snapshot: A3DMSnapshot):
        self._snapshot = snapshot

    def relations_for(self, root: str, classname: str) -> dict[str, Any]:
        local = self._snapshot.get_class(root, classname)
        resolved = self._snapshot.resolved_properties(root, classname)
        parent_name = local.get("parent")
        parent = None
        if isinstance(parent_name, str) and parent_name:
            parent = A3RelationTarget(root, parent_name, self._exists(root, parent_name)).to_dict()

        children = [
            A3RelationTarget(root, child, True).to_dict()
            for child in self._snapshot.class_names(root)
            if self._snapshot.get_class(root, child).get("parent") == classname
        ]

        outbound: dict[str, list[dict[str, Any]]] = {}
        for property_name, target_root in RELATION_TARGET_ROOTS.items():
            names = self._class_names(resolved.get(property_name))
            outbound[property_name] = [
                A3RelationTarget(target_root, name, self._exists(target_root, name)).to_dict()
                for name in names
            ]

        missing = [
            {"relation": relation, **target}
            for relation, targets in outbound.items()
            for target in targets
            if not target["exists"]
        ]
        if parent is not None and not parent["exists"]:
            missing.insert(0, {"relation": "parent", **parent})

        return {
            "parent": parent,
            "children": children,
            "outbound": outbound,
            "missingTargets": missing,
            "complete": not missing,
        }

    def _exists(self, root: str, classname: str) -> bool:
        return self._snapshot.has_root(root) and classname in self._snapshot.class_names(root)

    @staticmethod
    def _class_names(value: Any) -> tuple[str, ...]:
        if isinstance(value, str):
            return (value,) if value else ()
        if isinstance(value, (list, tuple)):
            return tuple(item for item in value if isinstance(item, str) and item)
        return ()
