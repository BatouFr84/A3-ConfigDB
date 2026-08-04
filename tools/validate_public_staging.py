#!/usr/bin/env python3
"""Fail-closed validation gate for the sanitized public A3-ConfigDB staging tree."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DENIED_PATH_PARTS = {
    "v008",
    "total_v2",
    "canonical",
    "v2_build",
    "v2_cdlc_build",
    "rpt",
    ".env",
    "render.yaml",
}

DENIED_TEXT_PATTERNS = {
    "A3CDB_AUTH_PASSWORD": re.compile(r"A3CDB_AUTH_PASSWORD", re.I),
    "PRIVATE_KEY": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "GITHUB_TOKEN_ASSIGNMENT": re.compile(r"GITHUB_TOKEN\s*[:=]\s*[^\s$]", re.I),
    "TOTAL_V2_DATA_REFERENCE": re.compile(r"(?:data/|\\b)(?:TOTAL_V2|v2_cdlc_build|v2_build)(?:/|\\b)", re.I),
}

TEXT_SUFFIXES = {
    ".css", ".csv", ".html", ".ini", ".js", ".json", ".md", ".py",
    ".sqf", ".txt", ".toml", ".yaml", ".yml",
}

REQUIRED_FILES = {
    "README.md",
    "LICENSE",
    "NOTICE.md",
    "DATA_POLICY.md",
    "AI_DISCLOSURE.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "Dockerfile",
    "data/fixtures/public_fixture.json",
    "tools/a3cdb_query/public_fixture_server.py",
    "tests/test_public_fixture.py",
    ".github/workflows/staging-validation.yml",
}

ALLOWED_FIXTURE_PREFIX = "A3CDB_Test_"
ALLOWED_PROFILE_IDS = {"P0_TEST", "P1_TEST"}


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def iter_files() -> list[Path]:
    return sorted(
        path for path in ROOT.rglob("*")
        if path.is_file() and ".git" not in path.parts and "__pycache__" not in path.parts
    )


def validate_license(errors: list[str]) -> None:
    license_path = ROOT / "LICENSE"
    if not license_path.exists():
        fail("LICENSE is missing", errors)
        return
    text = license_path.read_text(encoding="utf-8", errors="strict")
    required_markers = (
        "GNU AFFERO GENERAL PUBLIC LICENSE",
        "Version 3, 19 November 2007",
        "13. Remote Network Interaction; Use with the GNU General Public License.",
        "END OF TERMS AND CONDITIONS",
    )
    if len(text.encode("utf-8")) < 30_000:
        fail("LICENSE is not the complete AGPL-3.0 text (file is too short)", errors)
    for marker in required_markers:
        if marker not in text:
            fail(f"LICENSE missing marker: {marker}", errors)
    if "must replace this staging notice" in text.lower():
        fail("LICENSE still contains the staging replacement notice", errors)


def validate_fixture(errors: list[str]) -> None:
    path = ROOT / "data/fixtures/public_fixture.json"
    if not path.exists():
        fail("Public fixture dataset is missing", errors)
        return
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"Public fixture dataset is invalid JSON: {exc}", errors)
        return

    if payload.get("artificialDataOnly") is not True:
        fail("Fixture dataset must declare artificialDataOnly=true", errors)
    if payload.get("sourceGameDataIncluded") is not False:
        fail("Fixture dataset must declare sourceGameDataIncluded=false", errors)

    profiles = payload.get("profiles")
    if not isinstance(profiles, list) or not profiles:
        fail("Fixture dataset profiles must be a non-empty list", errors)
        return

    found_profiles = set()
    for profile in profiles:
        profile_id = profile.get("profileId")
        found_profiles.add(profile_id)
        if profile_id not in ALLOWED_PROFILE_IDS:
            fail(f"Unexpected fixture profile: {profile_id!r}", errors)
        for asset in profile.get("assets", []):
            class_name = asset.get("className", "")
            if not class_name.startswith(ALLOWED_FIXTURE_PREFIX):
                fail(f"Non-artificial fixture classname: {class_name!r}", errors)

    if found_profiles != ALLOWED_PROFILE_IDS:
        fail(f"Fixture profiles mismatch: {sorted(found_profiles)}", errors)


def validate_tree(errors: list[str]) -> None:
    files = iter_files()
    relative_paths = {path.relative_to(ROOT).as_posix() for path in files}

    for required in sorted(REQUIRED_FILES - relative_paths):
        fail(f"Required public file missing: {required}", errors)

    for path in files:
        relative = path.relative_to(ROOT).as_posix()
        lowered_parts = {part.lower() for part in Path(relative).parts}
        for denied in DENIED_PATH_PARTS:
            if denied.lower() in lowered_parts:
                fail(f"Denied path component {denied!r}: {relative}", errors)

        if path.is_symlink():
            fail(f"Symlink is forbidden: {relative}", errors)
            continue

        if path.stat().st_size > 5_000_000:
            fail(f"File exceeds 5 MB public limit: {relative}", errors)

        if path.suffix.lower() in TEXT_SUFFIXES or path.name in {"Dockerfile", "LICENSE"}:
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                fail(f"Text file is not valid UTF-8: {relative}", errors)
                continue
            for label, pattern in DENIED_TEXT_PATTERNS.items():
                if pattern.search(text):
                    fail(f"Denied content {label} in {relative}", errors)


def main() -> int:
    errors: list[str] = []
    validate_tree(errors)
    validate_fixture(errors)
    validate_license(errors)

    if errors:
        print("PUBLIC_STAGING_VALIDATION=REJECTED")
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("PUBLIC_STAGING_VALIDATION=PASS")
    print("DATA_BOUNDARY=PASS")
    print("ARTIFICIAL_FIXTURES=PASS")
    print("AGPL_LICENSE=PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
