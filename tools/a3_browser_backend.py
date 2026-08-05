#!/usr/bin/env python3
"""Browser-facing backend facade for A3-ConfigDB."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from tools.a3dm_snapshot import A3DMSnapshot
from tools.a3ql import A3QLSyntaxError
from tools.a3ql_runtime import A3QLExecutionError, A3QLRuntime
from tools.a3qm import A3QMError, normalize_query
from tools.a3qe import A3QEEngine, A3QEQueryError
from tools.a3qe_planner import A3QEPlan


@dataclass(frozen=True)
class BrowserBackendResponse:
    status: int
    body: Mapping[str, Any]


class A3BrowserBackend:
    """Stable JSON-oriented facade over A3QM, A3QL, and A3QE."""

    def __init__(self, snapshot: A3DMSnapshot):
        self._snapshot = snapshot
        self._engine = A3QEEngine(snapshot)
        self._runtime = A3QLRuntime(snapshot)

    def capabilities(self) -> BrowserBackendResponse:
        return self._ok({
            "snapshot": self._snapshot_metadata(),
            "queryModes": ["basic", "advanced"],
            "operators": ["eq", "contains"],
            "textIndexedFields": list(self._engine.text_indexed_fields),
            "planner": {
                "indexes": ["exact", "property", "text"],
                "completeResultsOnly": True,
                "silentFallback": False,
            },
            "maxLimit": 500,
        })

    def execute_basic(self, payload: Mapping[str, Any]) -> BrowserBackendResponse:
        try:
            normalized = normalize_query(payload)
            results = self._engine.execute(normalized.to_a3qe())
            plan = self._engine.last_plan
            if plan is None:
                raise A3QEQueryError("query plan was not produced")
        except A3QMError as exc:
            return self._error(400, "QUERY_VALIDATION_ERROR", str(exc))
        except A3QEQueryError as exc:
            return self._error(422, "QUERY_EXECUTION_ERROR", str(exc))
        return self._results("basic", results, normalized.limit, plan)

    def execute_advanced(self, source: str) -> BrowserBackendResponse:
        try:
            execution = self._runtime.execute(source)
        except A3QLSyntaxError as exc:
            return self._error(400, "A3QL_SYNTAX_ERROR", str(exc))
        except A3QLExecutionError as exc:
            return self._error(422, "A3QL_EXECUTION_ERROR", str(exc))
        return self._results("advanced", execution.results, execution.limit, execution.plan)

    def _results(self, mode: str, results: Any, limit: int, plan: A3QEPlan) -> BrowserBackendResponse:
        items = [{"root": item.root, "classname": item.classname} for item in results]
        return self._ok({
            "mode": mode,
            "snapshot": self._snapshot_metadata(),
            "limit": limit,
            "count": len(items),
            "executionPlan": plan.to_dict(),
            "results": items,
        })

    def _snapshot_metadata(self) -> Mapping[str, Any]:
        manifest = self._snapshot.manifest
        return {
            "snapshotId": self._snapshot.snapshot_id,
            "gameVersion": self._snapshot.game_version,
            "presetLabel": self._snapshot.preset_label,
            "schemaVersion": manifest["schemaVersion"],
            "roots": list(self._snapshot.roots),
        }

    @staticmethod
    def _ok(data: Mapping[str, Any]) -> BrowserBackendResponse:
        return BrowserBackendResponse(200, {"status": "ok", "data": data})

    @staticmethod
    def _error(status: int, code: str, message: str) -> BrowserBackendResponse:
        return BrowserBackendResponse(status, {
            "status": "error",
            "error": {"code": code, "message": message},
        })
