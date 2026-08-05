#!/usr/bin/env python3
"""A3XE integrity and resume baseline.

This module persists deterministic extraction state, fingerprints the extraction
context and validates final A3DM output before publication.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any, Mapping

from tools.a3dm_snapshot import A3DMSnapshot, A3DMSnapshotError
from tools.a3xe_artificial_exporter import canonical_json, snapshot_digest


class A3XEResumeError(ValueError):
    pass


class A3XEIntegrityError(ValueError):
    pass


IMMUTABLE_CONTEXT_FIELDS = (
    "gameVersion",
    "gameBuild",
    "loadedAddons",
    "activeDlc",
    "roots",
    "propertyMode",
    "inheritanceMode",
    "relationMode",
)


def context_fingerprint(context: Mapping[str, Any]) -> str:
    """Return a stable SHA-256 fingerprint for the resume-critical context."""
    normalized = {field: context.get(field) for field in IMMUTABLE_CONTEXT_FIELDS}
    return hashlib.sha256(canonical_json(normalized).encode("utf-8")).hexdigest()


def new_resume_state(*, run_id: str, context: Mapping[str, Any]) -> dict[str, Any]:
    roots = list(context.get("roots", []))
    return {
        "stateVersion": "0.1",
        "runId": run_id,
        "status": "running",
        "context": dict(context),
        "contextFingerprint": context_fingerprint(context),
        "progress": {
            "rootsTotal": len(roots),
            "rootsComplete": 0,
            "classesDiscovered": 0,
            "classesSerialized": 0,
            "lastRoot": None,
            "lastClassname": None,
        },
        "resumePossible": True,
        "integrityState": "pending",
    }


def validate_resume_context(state: Mapping[str, Any], context: Mapping[str, Any]) -> None:
    expected = state.get("contextFingerprint")
    actual = context_fingerprint(context)
    if expected != actual:
        changed = [
            field
            for field in IMMUTABLE_CONTEXT_FIELDS
            if state.get("context", {}).get(field) != context.get(field)
        ]
        detail = ", ".join(changed) if changed else "unknown context difference"
        raise A3XEResumeError(f"resume context mismatch: {detail}")
    if state.get("status") == "complete":
        raise A3XEResumeError("completed extraction cannot be resumed")
    if state.get("resumePossible") is not True:
        raise A3XEResumeError("resume is disabled for this extraction state")


def checkpoint(
    state: Mapping[str, Any],
    *,
    root: str,
    classname: str,
    classes_discovered: int,
    classes_serialized: int,
    roots_complete: int,
) -> dict[str, Any]:
    updated = json.loads(json.dumps(state))
    progress = updated["progress"]
    if classes_serialized < progress.get("classesSerialized", 0):
        raise A3XEResumeError("classesSerialized cannot move backwards")
    if roots_complete < progress.get("rootsComplete", 0):
        raise A3XEResumeError("rootsComplete cannot move backwards")
    if classes_serialized > classes_discovered:
        raise A3XEResumeError("classesSerialized cannot exceed classesDiscovered")
    if roots_complete > progress.get("rootsTotal", 0):
        raise A3XEResumeError("rootsComplete cannot exceed rootsTotal")
    progress.update(
        {
            "rootsComplete": roots_complete,
            "classesDiscovered": classes_discovered,
            "classesSerialized": classes_serialized,
            "lastRoot": root,
            "lastClassname": classname,
        }
    )
    return updated


def write_state_atomic(path: str | Path, state: Mapping[str, Any]) -> Path:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".tmp")
    temporary.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, destination)
    return destination


def load_state(path: str | Path) -> dict[str, Any]:
    source = Path(path)
    try:
        value = json.loads(source.read_text(encoding="utf-8"))
    except OSError as exc:
        raise A3XEResumeError(f"cannot read resume state: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise A3XEResumeError(f"invalid resume state JSON: {exc}") from exc
    if not isinstance(value, dict) or value.get("stateVersion") != "0.1":
        raise A3XEResumeError("unsupported resume state")
    return value


def verify_snapshot_integrity(package: Mapping[str, Any], expected_classes: int) -> dict[str, Any]:
    try:
        snapshot = A3DMSnapshot(package)
    except A3DMSnapshotError as exc:
        raise A3XEIntegrityError(str(exc)) from exc

    actual_classes = sum(len(snapshot.class_names(root)) for root in snapshot.roots)
    if actual_classes != expected_classes:
        raise A3XEIntegrityError(
            f"class count mismatch: expected {expected_classes}, got {actual_classes}"
        )

    for root in snapshot.roots:
        class_names = set(snapshot.class_names(root))
        for classname in class_names:
            parent = snapshot.get_class(root, classname).get("parent")
            if parent is not None and parent not in class_names:
                raise A3XEIntegrityError(f"missing parent: {root}/{classname} -> {parent}")
            snapshot.resolved_properties(root, classname)

    digest = snapshot_digest(package)
    return {
        "algorithm": "sha256",
        "snapshotDigest": digest,
        "classesValidated": actual_classes,
        "rootsValidated": len(snapshot.roots),
        "complete": True,
        "canonicalJson": True,
    }


def complete_state(state: Mapping[str, Any], package: Mapping[str, Any]) -> dict[str, Any]:
    progress = state.get("progress", {})
    if progress.get("rootsComplete") != progress.get("rootsTotal"):
        raise A3XEIntegrityError("not all roots are complete")
    if progress.get("classesSerialized") != progress.get("classesDiscovered"):
        raise A3XEIntegrityError("not all discovered classes are serialized")

    integrity = verify_snapshot_integrity(package, int(progress.get("classesSerialized", 0)))
    updated = json.loads(json.dumps(state))
    updated["status"] = "complete"
    updated["resumePossible"] = False
    updated["integrityState"] = "verified"
    updated["integrity"] = integrity
    return updated
