from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "data" / "fixtures" / "public_fixture.json"
WEB = ROOT / "web"
DATA = json.loads(FIXTURE.read_text(encoding="utf-8"))


def _json(handler: BaseHTTPRequestHandler, status: int, payload: object) -> None:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args: object) -> None:
        print(f"{self.address_string()} - {fmt % args}")

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/healthz":
            return _json(self, 200, {"status": "ok", "dataset": "artificial"})
        if path == "/api/capabilities":
            return _json(self, 200, {
                "mode": "PUBLIC_FIXTURE_ONLY",
                "profiles": [p["profileId"] for p in DATA["profiles"]],
                "realGameData": False,
                "basicSearch": True,
                "advancedA3QL": False
            })
        target = WEB / ("index.html" if path == "/" else path.lstrip("/"))
        if not target.is_file() or WEB not in target.resolve().parents:
            return _json(self, 404, {"error": "not_found"})
        body = target.read_bytes()
        content_type = "text/html; charset=utf-8" if target.suffix == ".html" else "text/plain; charset=utf-8"
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:
        if urlparse(self.path).path != "/api/basic":
            return _json(self, 404, {"error": "not_found"})
        try:
            length = min(int(self.headers.get("Content-Length", "0")), 65536)
            request = json.loads(self.rfile.read(length) or b"{}")
            profile_id = str(request.get("profile", "P0_TEST"))
            root = str(request.get("root", "")).strip()
            field = str(request.get("field", "className"))
            value = str(request.get("value", "")).casefold()
            limit = max(1, min(int(request.get("limit", 100)), 500))
            profile = next(p for p in DATA["profiles"] if p["profileId"] == profile_id)
            records = []
            for asset in profile["assets"]:
                if root and asset["configRoot"] != root:
                    continue
                candidate = asset.get(field, asset.get("properties", {}).get(field, ""))
                if value and value not in json.dumps(candidate, ensure_ascii=False).casefold():
                    continue
                records.append(asset)
                if len(records) >= limit:
                    break
            return _json(self, 200, {"profile": profile_id, "records": records, "returned": len(records)})
        except (ValueError, KeyError, StopIteration, json.JSONDecodeError) as exc:
            return _json(self, 400, {"error": "invalid_request", "message": str(exc)})


def main() -> None:
    port = int(os.environ.get("PORT", "8080"))
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    print(f"A3-ConfigDB public fixture server listening on 0.0.0.0:{port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
