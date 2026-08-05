#!/usr/bin/env python3
"""Convert one controlled A3XE SQF capture into A3DM and A3XE run files."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Mapping

from tools.a3dm_snapshot import A3DMSnapshot


class A3XESQFCaptureError(ValueError):
    pass


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _digest(value: Mapping[str, Any]) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def convert_capture(capture: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    if capture.get("captureVersion") != "0.1":
        raise A3XESQFCaptureError("unsupported captureVersion")
    if capture.get("source") != "arma3_sqf":
        raise A3XESQFCaptureError("capture source must be arma3_sqf")

    root = capture.get("root")
    classes_source = capture.get("classes")
    game = capture.get("game")
    if root != "CfgWeapons":
        raise A3XESQFCaptureError("PUB039 supports only CfgWeapons")
    if not isinstance(classes_source, list) or not isinstance(game, Mapping):
        raise A3XESQFCaptureError("capture requires classes and game metadata")

    classes: dict[str, Any] = {}
    for item in classes_source:
        if not isinstance(item, Mapping):
            raise A3XESQFCaptureError("each class must be an object")
        classname = item.get("classname")
        parent = item.get("parent")
        properties = item.get("properties", {})
        if not isinstance(classname, str) or not classname:
            raise A3XESQFCaptureError("classname must be a non-empty string")
        if classname in classes:
            raise A3XESQFCaptureError(f"duplicate classname: {classname}")
        if parent is not None and not isinstance(parent, str):
            raise A3XESQFCaptureError(f"invalid parent: {classname}")
        if not isinstance(properties, Mapping):
            raise A3XESQFCaptureError(f"properties must be an object: {classname}")
        unsupported = set(properties) - {"displayName", "scope", "author", "dlc"}
        if unsupported:
            raise A3XESQFCaptureError(f"unsupported properties for {classname}: {sorted(unsupported)}")
        classes[classname] = {"parent": parent, "properties": dict(properties)}

    for classname, item in classes.items():
        parent = item["parent"]
        if parent is not None and parent not in classes:
            raise A3XESQFCaptureError(f"parent outside controlled capture: {classname} -> {parent}")

    ordered_classes = {name: classes[name] for name in sorted(classes)}
    artificial = bool(capture.get("artificial", False))
    snapshot_id = str(capture.get("snapshotId", "A3XE_SQF_CAPTURE_V0_1"))
    package = {
        "manifest": {
            "format": "A3DM",
            "schemaVersion": "0.1",
            "packageVersion": "0.1.0-sqf-prototype",
            "datasetId": str(capture.get("datasetId", "A3XE_SQF_CONTROLLED_DATASET")),
            "snapshotId": snapshot_id,
            "createdAt": str(capture.get("createdAt", "1970-01-01T00:00:00Z")),
            "extractorVersion": "A3XE-SQF-0.1",
            "gameVersion": str(game.get("version", "unknown")),
            "presetLabel": str(capture.get("presetLabel", "Controlled SQF capture")),
            "loadedAddons": list(capture.get("loadedAddons", [])),
            "activeDlc": list(capture.get("activeDlc", [])),
            "artificialDataOnly": artificial,
            "sourceGameDataIncluded": not artificial,
        },
        "snapshot": {"snapshotId": snapshot_id, "roots": {root: ordered_classes}},
    }

    snapshot = A3DMSnapshot(package)
    class_names = snapshot.class_names(root)
    envelope = {
        "contractVersion": "0.1",
        "run": {
            "runId": str(capture.get("runId", "A3XE_SQF_RUN_V0_1")),
            "extractorVersion": "A3XE-SQF-0.1",
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
            "roots": [root],
            "propertyMode": "local",
            "inheritanceMode": "explicit_parent",
            "relationMode": "none",
        },
        "progress": {
            "rootsTotal": 1,
            "rootsComplete": 1,
            "classesDiscovered": len(class_names),
            "classesSerialized": len(class_names),
            "lastRoot": root,
            "lastClassname": class_names[-1] if class_names else None,
        },
        "integrity": {
            "algorithm": "sha256",
            "snapshotDigest": _digest(package),
            "complete": True,
            "canonicalJson": True,
        },
        "diagnostics": {"errors": [], "warnings": [], "skipped": []},
    }
    return package, envelope


def write_conversion(capture_path: str | Path, output_dir: str | Path) -> tuple[Path, Path]:
    capture = json.loads(Path(capture_path).read_text(encoding="utf-8"))
    package, envelope = convert_capture(capture)
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
    print("A3XE_SQF_CONVERSION=PASS")
    print(f"SNAPSHOT={snapshot}")
    print(f"RUN={run}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
