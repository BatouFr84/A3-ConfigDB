#!/usr/bin/env python3
"""PUB042 SQF converter exposing local and resolved properties."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any, Mapping

from tools.a3xe_resolved_properties import (
    A3XEResolvedPropertyError,
    resolve_properties,
)
from tools.a3xe_sqf_capture_converter import A3XESQFCaptureError
from tools.a3xe_sqf_inheritance_converter import convert_capture_with_inheritance


def convert_capture_with_resolved_properties(
    capture: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    try:
        package, envelope = convert_capture_with_inheritance(capture)
        root = str(capture["root"])
        classes = package["snapshot"]["roots"][root]
        properties = resolve_properties(classes)
    except (A3XEResolvedPropertyError, KeyError, TypeError, ValueError) as exc:
        if isinstance(exc, A3XESQFCaptureError):
            raise
        raise A3XESQFCaptureError(str(exc)) from exc

    envelope["selection"]["propertyMode"] = "local_and_resolved"
    envelope["resolvedProperties"] = {
        "root": root,
        "complete": True,
        "classes": properties,
    }
    return package, envelope


def write_conversion(capture_path: str | Path, output_dir: str | Path) -> tuple[Path, Path]:
    capture = json.loads(Path(capture_path).read_text(encoding="utf-8"))
    package, envelope = convert_capture_with_resolved_properties(capture)
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    snapshot_path = destination / "snapshot.a3dm.json"
    run_path = destination / "a3xe-run.json"
    for path, value in ((snapshot_path, package), (run_path, envelope)):
        temporary = path.with_suffix(path.suffix + ".tmp")
        temporary.write_text(
            json.dumps(value, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        os.replace(temporary, path)
    return snapshot_path, run_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("capture")
    parser.add_argument("output_dir")
    args = parser.parse_args()
    snapshot, run = write_conversion(args.capture, args.output_dir)
    print("A3XE_SQF_RESOLVED_PROPERTY_CONVERSION=PASS")
    print(f"SNAPSHOT={snapshot}")
    print(f"RUN={run}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
