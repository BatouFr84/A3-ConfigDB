from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from tools.a3_browser_backend import A3BrowserBackend
from tools.a3dm_snapshot import A3DMSnapshot, A3DMSnapshotError
from tools.a3_relations import A3RelationResolver


@dataclass(frozen=True)
class ApplicationResponse:
    status: int
    body: Mapping[str, Any]


class A3ConfigDBApplication:
    """Transport-neutral local application service."""

    def __init__(self, snapshot: A3DMSnapshot | None, *, dataset_path: str | Path | None = None, load_error: str | None = None):
        self.snapshot = snapshot
        self.dataset_path = Path(dataset_path).resolve() if dataset_path is not None else None
        self.load_error = load_error
        self.backend = A3BrowserBackend(snapshot) if snapshot is not None else None
        self.relations = A3RelationResolver(snapshot) if snapshot is not None else None

    @classmethod
    def from_dataset(cls, dataset_path: str | Path) -> "A3ConfigDBApplication":
        source = Path(dataset_path)
        try:
            return cls(A3DMSnapshot.from_file(source), dataset_path=source)
        except A3DMSnapshotError as exc:
            return cls(None, dataset_path=source, load_error=str(exc))

    @property
    def dataset_loaded(self) -> bool:
        return self.snapshot is not None

    def health(self) -> ApplicationResponse:
        return ApplicationResponse(200, {"status": "ok", "application": "A3-ConfigDB", "datasetLoaded": self.dataset_loaded, "dataset": self.snapshot.snapshot_id if self.snapshot is not None else None})

    def dataset_status(self) -> ApplicationResponse:
        if self.snapshot is None:
            return ApplicationResponse(200, {"status": "ok", "data": {"loaded": False, "path": str(self.dataset_path) if self.dataset_path is not None else None, "error": self.load_error, "manifest": None}})
        class_count = sum(len(self.snapshot.class_names(root)) for root in self.snapshot.roots)
        return ApplicationResponse(200, {"status": "ok", "data": {"loaded": True, "path": str(self.dataset_path) if self.dataset_path is not None else None, "error": None, "snapshotId": self.snapshot.snapshot_id, "roots": list(self.snapshot.roots), "classCount": class_count, "manifest": dict(self.snapshot.manifest)}})

    def capabilities(self) -> ApplicationResponse:
        unavailable = self._require_dataset()
        if unavailable is not None:
            return unavailable
        assert self.backend is not None
        response = self.backend.capabilities()
        return ApplicationResponse(response.status, dict(response.body))

    def execute_basic(self, payload: Mapping[str, Any]) -> ApplicationResponse:
        unavailable = self._require_dataset()
        if unavailable is not None:
            return unavailable
        assert self.backend is not None
        response = self.backend.execute_basic(payload)
        return self._enrich_results(response.status, response.body)

    def execute_advanced(self, source: str) -> ApplicationResponse:
        unavailable = self._require_dataset()
        if unavailable is not None:
            return unavailable
        assert self.backend is not None
        response = self.backend.execute_advanced(source)
        return self._enrich_results(response.status, response.body)

    def get_class(self, root: str, classname: str) -> ApplicationResponse:
        unavailable = self._require_dataset()
        if unavailable is not None:
            return unavailable
        assert self.snapshot is not None and self.relations is not None
        try:
            local = self.snapshot.get_class(root, classname)
            resolved = self.snapshot.resolved_properties(root, classname)
            relations = self.relations.relations_for(root, classname)
        except A3DMSnapshotError as exc:
            return ApplicationResponse(404, {"status": "error", "error": {"code": "CLASS_NOT_FOUND", "message": str(exc)}})
        return ApplicationResponse(200, {"status": "ok", "data": {"root": root, "classname": classname, "parent": local.get("parent"), "localProperties": dict(local.get("properties", {})), "resolvedProperties": dict(resolved), "relations": relations}})

    def _require_dataset(self) -> ApplicationResponse | None:
        if self.snapshot is not None:
            return None
        return ApplicationResponse(503, {"status": "error", "error": {"code": "DATASET_NOT_LOADED", "message": self.load_error or "no dataset is loaded"}})

    def _enrich_results(self, status: int, source_body: Mapping[str, Any]) -> ApplicationResponse:
        assert self.snapshot is not None
        body = dict(source_body)
        data = body.get("data")
        if status == 200 and body.get("status") == "ok" and isinstance(data, Mapping) and "results" in data:
            enriched = []
            for item in data["results"]:
                root, classname = item["root"], item["classname"]
                local = self.snapshot.get_class(root, classname)
                resolved = self.snapshot.resolved_properties(root, classname)
                enriched.append({**item, "displayName": resolved.get("displayName"), "parent": local.get("parent")})
            body = {**body, "data": {**data, "results": enriched}}
        return ApplicationResponse(status, body)
