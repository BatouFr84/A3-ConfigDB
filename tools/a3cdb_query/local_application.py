from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from tools.a3_browser_backend import A3BrowserBackend
from tools.a3dm_snapshot import A3DMSnapshot, A3DMSnapshotError


@dataclass(frozen=True)
class ApplicationResponse:
    status: int
    body: Mapping[str, Any]


class A3ConfigDBApplication:
    """Transport-neutral local application service."""

    def __init__(self, snapshot: A3DMSnapshot):
        self.snapshot = snapshot
        self.backend = A3BrowserBackend(snapshot)

    @classmethod
    def from_dataset(cls, dataset_path: str | Path) -> "A3ConfigDBApplication":
        return cls(A3DMSnapshot.from_file(dataset_path))

    def health(self) -> ApplicationResponse:
        return ApplicationResponse(200, {
            "status": "ok",
            "application": "A3-ConfigDB",
            "dataset": self.snapshot.snapshot_id,
        })

    def capabilities(self) -> ApplicationResponse:
        response = self.backend.capabilities()
        return ApplicationResponse(response.status, dict(response.body))

    def execute_basic(self, payload: Mapping[str, Any]) -> ApplicationResponse:
        response = self.backend.execute_basic(payload)
        return self._enrich_results(response.status, response.body)

    def execute_advanced(self, source: str) -> ApplicationResponse:
        response = self.backend.execute_advanced(source)
        return self._enrich_results(response.status, response.body)

    def get_class(self, root: str, classname: str) -> ApplicationResponse:
        try:
            local = self.snapshot.get_class(root, classname)
            resolved = self.snapshot.resolved_properties(root, classname)
        except A3DMSnapshotError as exc:
            return ApplicationResponse(404, {
                "status": "error",
                "error": {"code": "CLASS_NOT_FOUND", "message": str(exc)},
            })
        return ApplicationResponse(200, {
            "status": "ok",
            "data": {
                "root": root,
                "classname": classname,
                "parent": local.get("parent"),
                "localProperties": dict(local.get("properties", {})),
                "resolvedProperties": dict(resolved),
            },
        })

    def _enrich_results(self, status: int, source_body: Mapping[str, Any]) -> ApplicationResponse:
        body = dict(source_body)
        data = body.get("data")
        if status == 200 and body.get("status") == "ok" and isinstance(data, Mapping) and "results" in data:
            enriched = []
            for item in data["results"]:
                root, classname = item["root"], item["classname"]
                local = self.snapshot.get_class(root, classname)
                resolved = self.snapshot.resolved_properties(root, classname)
                enriched.append({
                    **item,
                    "displayName": resolved.get("displayName"),
                    "parent": local.get("parent"),
                })
            body = {**body, "data": {**data, "results": enriched}}
        return ApplicationResponse(status, body)
