#!/usr/bin/env python3
"""Deterministic inheritance-chain reconstruction for A3XE captures."""

from __future__ import annotations

from typing import Any, Mapping


class A3XEInheritanceError(ValueError):
    pass


def build_inheritance_chains(classes: Mapping[str, Mapping[str, Any]]) -> dict[str, list[str]]:
    """Return root-to-class chains and reject missing parents or cycles."""
    chains: dict[str, list[str]] = {}

    def resolve(classname: str, visiting: tuple[str, ...] = ()) -> list[str]:
        if classname in chains:
            return chains[classname]
        if classname in visiting:
            cycle = " -> ".join((*visiting, classname))
            raise A3XEInheritanceError(f"inheritance cycle: {cycle}")
        item = classes.get(classname)
        if item is None:
            raise A3XEInheritanceError(f"missing class in inheritance graph: {classname}")
        parent = item.get("parent")
        if parent is None:
            chain = [classname]
        else:
            if not isinstance(parent, str) or not parent:
                raise A3XEInheritanceError(f"invalid parent: {classname}")
            if parent not in classes:
                raise A3XEInheritanceError(f"missing parent: {classname} -> {parent}")
            chain = [*resolve(parent, (*visiting, classname)), classname]
        chains[classname] = chain
        return chain

    for classname in sorted(classes):
        resolve(classname)
    return {name: chains[name] for name in sorted(chains)}
