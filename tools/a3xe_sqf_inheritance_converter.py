#!/usr/bin/env python3
"""PUB041 SQF converter with complete inheritance-chain validation."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any, Mapping

from tools.a3dm_snapshot import A3DMSnapshotError
from tools.a3xe_inheritance import A3XEInheritanceError, build_inheritance_chains
from tools.a3xe_sqf_capture_converter import A3XESQFCaptureError, convert_capture


def convert_capture_with_inheritance(capture: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    try:
        package, envelope = convert_capture(capture)
    except A3DMSnapshotError as exc:
        raise A3XESQFCaptureError(str(exc)) from exc

    root = str(capture["root"])
    classes = package["snapshot"]["roots"][root]
    try:
        chains = build_inheritance_chains(classes)
    except A3XEInheritanceError as exc:
        raise A3XESQFCaptureError(str(exc)) from exc
    envelope["inheritance"] = {
        "root": root,
        "complete": True,
        "chains": chains,
        "maxDepth": max((len(chain) for chain in chains.values()), default=0),
    }
    return package, envelope


def write_conversion(capture_path: str | Path, output_dir: str | Path) -> tuple[Path, Path]:
    capture = json.loads(Path(capture_path).read_text(encoding="utf-8"))
    package, envelope = convert_capture_with_inheritance(capture)
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
    print("A3XE_SQF_INHERITANCE_CONVERSION=PASS")
    print(f"SNAPSHOT={snapshot}")
    print(f"RUN={run}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
