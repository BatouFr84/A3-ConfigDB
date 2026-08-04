#!/usr/bin/env python3
"""Install and verify the official GNU AGPL v3 license text.

This helper is intentionally dependency-free. It downloads the canonical
license text from GNU, rejects HTML or truncated responses, writes LICENSE
atomically, and reports the resulting SHA-256 digest.
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
from urllib.request import Request, urlopen

SOURCE_URL = "https://www.gnu.org/licenses/agpl-3.0.txt"
TARGET = Path(__file__).resolve().parents[1] / "LICENSE"
REQUIRED_MARKERS = (
    "GNU AFFERO GENERAL PUBLIC LICENSE",
    "Version 3, 19 November 2007",
    "13. Remote Network Interaction; Use with the GNU General Public License.",
    "END OF TERMS AND CONDITIONS",
)
MINIMUM_BYTES = 30_000


def main() -> int:
    request = Request(SOURCE_URL, headers={"User-Agent": "A3-ConfigDB-license-installer/1"})
    with urlopen(request, timeout=30) as response:
        payload = response.read()

    text = payload.decode("utf-8")
    if len(payload) < MINIMUM_BYTES:
        raise SystemExit(f"Rejected truncated license payload: {len(payload)} bytes")
    for marker in REQUIRED_MARKERS:
        if marker not in text:
            raise SystemExit(f"Rejected license payload missing marker: {marker}")
    if "<html" in text.lower() or "<!doctype" in text.lower():
        raise SystemExit("Rejected HTML response instead of license text")

    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    if not normalized.endswith("\n"):
        normalized += "\n"

    temporary = TARGET.with_suffix(".tmp")
    temporary.write_text(normalized, encoding="utf-8", newline="\n")
    os.replace(temporary, TARGET)

    digest = hashlib.sha256(TARGET.read_bytes()).hexdigest()
    print(f"AGPL_INSTALL_OK path={TARGET} bytes={TARGET.stat().st_size} sha256={digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
