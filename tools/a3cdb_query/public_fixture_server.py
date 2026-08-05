from __future__ import annotations

import json
import mimetypes
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

from tools.a3_browser_backend import A3BrowserBackend
from tools.a3dm_snapshot import A3DMSnapshot

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "data" / "fixtures" / "a3dm_v0_1_example.json"
WEB = ROOT / "web"
SNAPSHOT = A3DMSnapshot.from_file(FIXTURE)
BACKEND = A3BrowserBackend(SNAPSHOT)


def _json(handler, status, payload):
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def _browser_response(handler, response):
    body = dict(response.body)
    if response.status == 200 and body.get("status") == "ok" and "results" in body.get("data", {}):
        enriched = []
        for item in body["data"]["results"]:
            root, classname = item["root"], item["classname"]
            class_data = SNAPSHOT.get_class(root, classname)
            resolved = SNAPSHOT.resolved_properties(root, classname)
            enriched.append({**item, "displayName": resolved.get("displayName"), "parent": class_data.get("parent")})
        body = {**body, "data": {**body["data"], "results": enriched}}
    _json(handler, response.status, body)


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print(f"{self.address_string()} - {fmt % args}")

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/healthz":
            return _json(self, 200, {"status": "ok", "dataset": "artificial"})
        if path == "/api/capabilities":
            return _browser_response(self, BACKEND.capabilities())
        if path.startswith("/api/class/"):
            parts = path.split("/", 4)
            if len(parts) != 5:
                return _json(self, 400, {"status": "error", "error": {"code": "INVALID_CLASS_PATH", "message": "root and classname are required"}})
            root, classname = unquote(parts[3]), unquote(parts[4])
            try:
                local = SNAPSHOT.get_class(root, classname)
                resolved = SNAPSHOT.resolved_properties(root, classname)
            except KeyError as exc:
                return _json(self, 404, {"status": "error", "error": {"code": "CLASS_NOT_FOUND", "message": str(exc)}})
            return _json(self, 200, {"status": "ok", "data": {"root": root, "classname": classname, "parent": local.get("parent"), "localProperties": dict(local.get("properties", {})), "resolvedProperties": dict(resolved)}})
        target = WEB / ("index.html" if path == "/" else path.lstrip("/"))
        resolved = target.resolve()
        if not target.is_file() or (resolved != WEB.resolve() and WEB.resolve() not in resolved.parents):
            return _json(self, 404, {"error": "not_found"})
        body = target.read_bytes()
        content_type = mimetypes.guess_type(target.name)[0] or "application/octet-stream"
        self.send_response(200)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        path = urlparse(self.path).path
        if path not in {"/api/basic", "/api/advanced"}:
            return _json(self, 404, {"error": "not_found"})
        try:
            length = min(int(self.headers.get("Content-Length", "0")), 65536)
            payload = json.loads(self.rfile.read(length) or b"{}")
        except (ValueError, json.JSONDecodeError) as exc:
            return _json(self, 400, {"status": "error", "error": {"code": "INVALID_JSON", "message": str(exc)}})
        if path == "/api/basic":
            return _browser_response(self, BACKEND.execute_basic(payload))
        source = payload.get("query") if isinstance(payload, dict) else None
        if not isinstance(source, str):
            return _json(self, 400, {"status": "error", "error": {"code": "INVALID_A3QL_REQUEST", "message": "query must be a string"}})
        return _browser_response(self, BACKEND.execute_advanced(source))


def main():
    port = int(os.environ.get("PORT", "8080"))
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    print(f"A3-ConfigDB PUB027 listening on 0.0.0.0:{port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
