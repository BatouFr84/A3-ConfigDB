#!/usr/bin/env python3
"""Convert one deterministic multi-root A3XE capture into A3DM and A3XE outputs."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Mapping

from tools.a3dm_snapshot import A3DMSnapshot
from tools.a3xe_inheritance import build_inheritance_chains
from tools.a3xe_native_relations import build_native_relations
from tools.a3xe_resolved_properties import resolve_properties


SUPPORTED_ROOTS = ("CfgWeapons", "CfgMagazines", "CfgAmmo", "CfgVehicles")
SUPPORTED_PROPERTIES = {
    "displayName", "scope", "author", "dlc", "weapons", "magazines", "ammo"
}


class A3XEMultiRootError(ValueError):
    pass


def _canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _digest(value: Mapping[str, Any]) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _normalise_root(root: str, items: Any) -> dict[str, Any]:
    if root not in SUPPORTED_ROOTS:
        raise A3XEMultiRootError(f"unsupported root: {root}")
    if not isinstance(items, list):
        raise A3XEMultiRootError(f"root classes must be an array: {root}")

    classes: dict[str, Any] = {}
    for item in items:
        if not isinstance(item, Mapping):
            raise A3XEMultiRootError(f"class must be an object: {root}")
        classname = item.get("classname")
        parent = item.get("parent")
        properties = item.get("properties", {})
        if not isinstance(classname, str) or not classname:
            raise A3XEMultiRootError(f"invalid classname: {root}")
        if classname in classes:
            raise A3XEMultiRootError(f"duplicate classname: {root}/{classname}")
        if parent is not None and (not isinstance(parent, str) or not parent):
            raise A3XEMultiRootError(f"invalid parent: {root}/{classname}")
        if not isinstance(properties, Mapping):
            raise A3XEMultiRootError(f"properties must be an object: {root}/{classname}")
        unsupported = set(properties) - SUPPORTED_PROPERTIES
        if unsupported:
            raise A3XEMultiRootError(
                f"unsupported properties for {root}/{classname}: {sorted(unsupported)}"
            )
        classes[classname] = {"parent": parent, "properties": dict(properties)}

    for classname, item in classes.items():
        parent = item["parent"]
        if parent is not None and parent not in classes:
            raise A3XEMultiRootError(f"missing parent: {root}/{classname} -> {parent}")
    return {name: classes[name] for name in sorted(classes)}


def convert_multi_root_capture(capture: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    if capture.get("captureVersion") != "0.2":
        raise A3XEMultiRootError("unsupported captureVersion")
    if capture.get("source") != "arma3_sqf":
        raise A3XEMultiRootError("capture source must be arma3_sqf")

    roots_source = capture.get("roots")
    game = capture.get("game")
    if not isinstance(roots_source, Mapping) or not isinstance(game, Mapping):
        raise A3XEMultiRootError("capture requires roots and game metadata")
    if not roots_source:
        raise A3XEMultiRootError("capture must contain at least one root")

    roots: dict[str, Any] = {}
    inheritance: dict[str, Any] = {}
    resolved_by_root: dict[str, Any] = {}
    classes_total = 0

    for root in sorted(roots_source):
        classes = _normalise_root(root, roots_source[root])
        roots[root] = classes
        inheritance[root] = build_inheritance_chains(classes)
        resolved_by_root[root] = resolve_properties(classes)
        classes_total += len(classes)

    snapshot_id = str(capture.get("snapshotId", "A3XE_MULTI_ROOT_V0_1"))
    package = {
        "manifest": {
            "format": "A3DM",
            "schemaVersion": "0.1",
            "packageVersion": "0.1.0-multi-root",
            "datasetId": str(capture.get("datasetId", "A3XE_MULTI_ROOT_DATASET")),
            "snapshotId": snapshot_id,
            "createdAt": str(capture.get("createdAt", "1970-01-01T00:00:00Z")),
            "extractorVersion": "A3XE-SQF-0.2",
            "gameVersion": str(game.get("version", "unknown")),
            "presetLabel": str(capture.get("presetLabel", "Controlled multi-root capture")),
            "loadedAddons": list(capture.get("loadedAddons", [])),
            "activeDlc": list(capture.get("activeDlc", [])),
            "artificialDataOnly": bool(capture.get("artificial", False)),
            "sourceGameDataIncluded": not bool(capture.get("artificial", False)),
        },
        "snapshot": {"snapshotId": snapshot_id, "roots": roots},
    }

    snapshot = A3DMSnapshot(package)
    relations = build_native_relations(roots, resolved_by_root)
    root_names = list(snapshot.roots)
    last_root = root_names[-1] if root_names else None
    last_classname = snapshot.class_names(last_root)[-1] if last_root and snapshot.class_names(last_root) else None

    envelope = {
        "contractVersion": "0.1",
        "run": {
            "runId": str(capture.get("runId", "A3XE_MULTI_ROOT_RUN_V0_1")),
            "extractorVersion": "A3XE-SQF-0.2",
            "startedAt": str(capture.get("startedAt", package["manifest"]["createdAt"])),
            "completedAt": str(capture.get("completedAt", package["manifest"]["createdAt"])),
            "status": "complete",
            "resumeOf": None,
        },
        "environment": {
            "game": dict(game),
            "platform": str(capture.get("platform", "unknown")),
            "language": str(capture.get("language", "unknown")),
            "loadedAddons": list(capture.get("loadedAddons", [])),
            "activeDlc": list(capture.get("activeDlc", [])),
        },
        "selection": {
            "roots": root_names,
            "propertyMode": "local_and_resolved",
            "inheritanceMode": "explicit_parent",
            "relationMode": "known_fields",
        },
        "progress": {
            "rootsTotal": len(root_names),
            "rootsComplete": len(root_names),
            "classesDiscovered": classes_total,
            "classesSerialized": classes_total,
            "lastRoot": last_root,
            "lastClassname": last_classname,
        },
        "integrity": {
            "algorithm": "sha256",
            "snapshotDigest": _digest(package),
            "complete": True,
            "canonicalJson": True,
        },
        "inheritance": {"complete": True, "roots": inheritance},
        "resolvedProperties": {"complete": True, "roots": resolved_by_root},
        "nativeRelations": relations,
        "diagnostics": {"errors": [], "warnings": [], "skipped": []},
    }
    return package, envelope


def write_conversion(capture_path: str | Path, output_dir: str | Path) -> tuple[Path, Path]:
    capture = json.loads(Path(capture_path).read_text(encoding="utf-8"))
    package, envelope = convert_multi_root_capture(capture)
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    snapshot_path = destination / "snapshot.a3dm.json"
    run_path = destination / "a3xe-run.json"
    for path, value in ((snapshot_path, package), (run_path, envelope)):
        temporary = path.with_suffix(path.suffix + ".tmp")
        temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        os.replace(temporary, path)
    return snapshot_path, run_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("capture")
    parser.add_argument("output_dir")
    args = parser.parse_args()
    snapshot, run = write_conversion(args.capture, args.output_dir)
    print("A3XE_MULTI_ROOT_CONVERSION=PASS")
    print(f"SNAPSHOT={snapshot}")
    print(f"RUN={run}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
