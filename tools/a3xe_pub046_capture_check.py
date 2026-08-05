#!/usr/bin/env python3
"""Validate one real PUB046 clipboard capture before conversion."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping

from tools.a3xe_sqf_capture_converter import A3XESQFCaptureError, convert_capture


class PUB046CaptureCheckError(ValueError):
    pass


def check_capture(capture: Mapping[str, Any]) -> dict[str, Any]:
    if capture.get("captureVersion") != "0.1":
        raise PUB046CaptureCheckError("unsupported captureVersion")
    if capture.get("source") != "arma3_sqf":
        raise PUB046CaptureCheckError("source must be arma3_sqf")
    if capture.get("artificial") is not False:
        raise PUB046CaptureCheckError("capture must declare artificial=false")
    if capture.get("root") != "CfgWeapons":
        raise PUB046CaptureCheckError("PUB046 expects CfgWeapons")

    classes = capture.get("classes")
    if not isinstance(classes, list) or not classes:
        raise PUB046CaptureCheckError("capture must contain at least one class")

    game = capture.get("game")
    if not isinstance(game, Mapping):
        raise PUB046CaptureCheckError("game metadata missing")
    for field in ("product", "version", "build"):
        value = game.get(field)
        if not isinstance(value, str) or not value:
            raise PUB046CaptureCheckError(f"game.{field} missing")

    try:
        package, envelope = convert_capture(capture)
    except A3XESQFCaptureError as exc:
        raise PUB046CaptureCheckError(str(exc)) from exc

    class_count = envelope["progress"]["classesSerialized"]
    return {
        "status": "PASS",
        "root": capture["root"],
        "classes": class_count,
        "gameVersion": game["version"],
        "gameBuild": game["build"],
        "snapshotId": package["manifest"]["snapshotId"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("capture")
    args = parser.parse_args()

    path = Path(args.capture)
    try:
        capture = json.loads(path.read_text(encoding="utf-8"))
        result = check_capture(capture)
    except (OSError, json.JSONDecodeError, PUB046CaptureCheckError) as exc:
        print("A3XE_PUB046_CAPTURE_CHECK=FAIL")
        print(f"ERROR={exc}")
        return 1

    print("A3XE_PUB046_CAPTURE_CHECK=PASS")
    for key in ("root", "classes", "gameVersion", "gameBuild", "snapshotId"):
        print(f"{key.upper()}={result[key]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
