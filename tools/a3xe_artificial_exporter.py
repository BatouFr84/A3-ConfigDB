#!/usr/bin/env python3
"""Deterministic artificial A3XE exporter used before the SQF extractor exists."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Mapping

from tools.a3dm_snapshot import A3DMSnapshot


class A3XEArtificialExportError(ValueError):
    pass


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def snapshot_digest(package: Mapping[str, Any]) -> str:
    return hashlib.sha256(canonical_json(package).encode("utf-8")).hexdigest()


def _resolved_properties(classes: Mapping[str, Any], classname: str) -> dict[str, Any]:
    chain: list[Mapping[str, Any]] = []
    current: str | None = classname
    visited: set[str] = set()
    while current is not None:
        if current in visited:
            raise A3XEArtificialExportError(f"inheritance cycle at: {classname}")
        visited.add(current)
        item = classes.get(current)
        if not isinstance(item, Mapping):
            raise A3XEArtificialExportError(f"missing parent class: {current}")
        chain.append(item)
        current = item.get("parent")
    resolved: dict[str, Any] = {}
    for item in reversed(chain):
        properties = item.get("properties", {})
        if not isinstance(properties, Mapping):
            raise A3XEArtificialExportError(f"properties must be an object: {classname}")
        resolved.update(properties)
    return resolved


def export_artificial(source: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    manifest_source = source.get("manifest")
    roots_source = source.get("roots")
    if not isinstance(manifest_source, Mapping) or not isinstance(roots_source, Mapping):
        raise A3XEArtificialExportError("source requires manifest and roots objects")

    roots: dict[str, Any] = {}
    classes_serialized = 0
    for root_name in sorted(roots_source):
        source_classes = roots_source[root_name]
        if not isinstance(source_classes, Mapping):
            raise A3XEArtificialExportError(f"root must be an object: {root_name}")
        root_output: dict[str, Any] = {}
        for classname in sorted(source_classes):
            item = source_classes[classname]
            if not isinstance(item, Mapping):
                raise A3XEArtificialExportError(f"class must be an object: {root_name}/{classname}")
            _resolved_properties(source_classes, classname)
            root_output[classname] = {
                "parent": item.get("parent"),
                "properties": dict(item.get("properties", {})),
            }
            classes_serialized += 1
        roots[root_name] = root_output

    snapshot_id = str(manifest_source["snapshotId"])
    package = {
        "manifest": {
            "format": "A3DM",
            "schemaVersion": "0.1",
            "packageVersion": str(manifest_source.get("packageVersion", "0.1.0-artificial")),
            "datasetId": str(manifest_source["datasetId"]),
            "snapshotId": snapshot_id,
            "createdAt": str(manifest_source["createdAt"]),
            "extractorVersion": str(manifest_source.get("extractorVersion", "A3XE-Artificial-0.1")),
            "gameVersion": str(manifest_source["gameVersion"]),
            "presetLabel": str(manifest_source["presetLabel"]),
            "loadedAddons": list(manifest_source.get("loadedAddons", [])),
            "activeDlc": list(manifest_source.get("activeDlc", [])),
            "artificialDataOnly": True,
            "sourceGameDataIncluded": False,
        },
        "snapshot": {"snapshotId": snapshot_id, "roots": roots},
    }

    snapshot = A3DMSnapshot(package)
    digest = snapshot_digest(package)
    root_names = list(snapshot.roots)
    last_root = root_names[-1] if root_names else None
    last_classname = snapshot.class_names(last_root)[-1] if last_root else None
    envelope = {
        "contractVersion": "0.1",
        "run": {
            "runId": str(source["runId"]),
            "extractorVersion": package["manifest"]["extractorVersion"],
            "startedAt": str(source["startedAt"]),
            "completedAt": str(source["completedAt"]),
            "status": "complete",
            "resumeOf": None,
        },
        "environment": dict(source["environment"]),
        "selection": {
            "roots": root_names,
            "propertyMode": "local_and_resolved",
            "inheritanceMode": "explicit_parent",
            "relationMode": "known_fields",
        },
        "progress": {
            "rootsTotal": len(root_names),
            "rootsComplete": len(root_names),
            "classesDiscovered": classes_serialized,
            "classesSerialized": classes_serialized,
            "lastRoot": last_root,
            "lastClassname": last_classname,
        },
        "integrity": {
            "algorithm": "sha256",
            "snapshotDigest": digest,
            "complete": True,
            "canonicalJson": True,
        },
        "diagnostics": {"errors": [], "warnings": [], "skipped": []},
    }
    return package, envelope


def write_export(source_path: str | Path, output_dir: str | Path) -> tuple[Path, Path]:
    source = json.loads(Path(source_path).read_text(encoding="utf-8"))
    package, envelope = export_artificial(source)
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
    parser.add_argument("source")
    parser.add_argument("output_dir")
    args = parser.parse_args()
    snapshot_path, run_path = write_export(args.source, args.output_dir)
    print("A3XE_ARTIFICIAL_EXPORT=PASS")
    print(f"SNAPSHOT={snapshot_path}")
    print(f"RUN={run_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
