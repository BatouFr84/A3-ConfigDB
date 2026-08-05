from __future__ import annotations

import json
import mimetypes
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

from tools.a3cdb_query.local_application import A3ConfigDBApplication, ApplicationResponse

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATASET = ROOT / "data" / "fixtures" / "a3dm_v0_1_example.json"
DEFAULT_WEB = ROOT / "web"
MAX_BODY_BYTES = 65536


def create_handler(application: A3ConfigDBApplication, web_root: Path = DEFAULT_WEB):
    web_root = web_root.resolve()

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt, *args):
            print(f"{self.address_string()} - {fmt % args}")

        def _json(self, response: ApplicationResponse):
            body = json.dumps(response.body, ensure_ascii=False).encode("utf-8")
            self.send_response(response.status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _error(self, status: int, code: str, message: str):
            self._json(ApplicationResponse(status, {
                "status": "error",
                "error": {"code": code, "message": message},
            }))

        def _read_json(self):
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if length < 0 or length > MAX_BODY_BYTES:
                    raise ValueError("request body exceeds the allowed size")
                return json.loads(self.rfile.read(length) or b"{}")
            except (ValueError, json.JSONDecodeError) as exc:
                self._error(400, "INVALID_JSON", str(exc))
                return None

        def do_GET(self):
            path = urlparse(self.path).path
            if path == "/healthz":
                return self._json(application.health())
            if path == "/api/dataset":
                return self._json(application.dataset_status())
            if path == "/api/capabilities":
                return self._json(application.capabilities())
            if path.startswith("/api/class/"):
                parts = path.split("/", 4)
                if len(parts) != 5:
                    return self._error(400, "INVALID_CLASS_PATH", "root and classname are required")
                return self._json(application.get_class(unquote(parts[3]), unquote(parts[4])))
            target = web_root / ("index.html" if path == "/" else path.lstrip("/"))
            resolved = target.resolve()
            if not target.is_file() or (resolved != web_root and web_root not in resolved.parents):
                return self._error(404, "NOT_FOUND", "resource not found")
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
                return self._error(404, "NOT_FOUND", "resource not found")
            payload = self._read_json()
            if payload is None:
                return
            if path == "/api/basic":
                if not isinstance(payload, dict):
                    return self._error(400, "INVALID_BASIC_REQUEST", "request body must be an object")
                return self._json(application.execute_basic(payload))
            source = payload.get("query") if isinstance(payload, dict) else None
            if not isinstance(source, str):
                return self._error(400, "INVALID_A3QL_REQUEST", "query must be a string")
            return self._json(application.execute_advanced(source))

    return Handler


def build_server(host: str, port: int, dataset_path: Path = DEFAULT_DATASET, web_root: Path = DEFAULT_WEB):
    application = A3ConfigDBApplication.from_dataset(dataset_path)
    return ThreadingHTTPServer((host, port), create_handler(application, web_root))


def main():
    host = os.environ.get("A3CDB_HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "8080"))
    dataset = Path(os.environ.get("A3CDB_DATASET", str(DEFAULT_DATASET)))
    application = A3ConfigDBApplication.from_dataset(dataset)
    server = ThreadingHTTPServer((host, port), create_handler(application, DEFAULT_WEB))
    print(f"A3-ConfigDB local application listening on http://{host}:{port}")
    if application.dataset_loaded:
        print(f"Dataset loaded: {dataset}")
    else:
        print(f"Dataset unavailable: {dataset}")
        print(f"Reason: {application.load_error}")
    server.serve_forever()


if __name__ == "__main__":
    main()
