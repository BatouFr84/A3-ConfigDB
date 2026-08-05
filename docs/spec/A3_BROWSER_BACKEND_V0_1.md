# A3 Browser Backend v0.1

PUB024 defines the transport-neutral backend contract used by the future local Browser.

## Scope

The backend accepts two query modes:

- `basic`: normalized A3QM payloads produced by form controls;
- `advanced`: raw A3QL text.

Both modes execute through A3QE and return the same result item shape.

## Success envelope

```json
{
  "status": "ok",
  "data": {
    "mode": "basic",
    "snapshot": {
      "snapshotId": "A3CDB_Test_Snapshot_01",
      "gameVersion": "A3CDB-Test-Game-1.0",
      "presetLabel": "Artificial test preset",
      "schemaVersion": "0.1",
      "roots": ["CfgVehicles", "CfgWeapons"]
    },
    "limit": 100,
    "count": 1,
    "results": [
      {"root": "CfgVehicles", "classname": "A3CDB_Test_Soldier"}
    ]
  }
}
```

## Error envelope

```json
{
  "status": "error",
  "error": {
    "code": "A3QL_SYNTAX_ERROR",
    "message": "expected identifier at position 4"
  }
}
```

Defined errors:

- `QUERY_VALIDATION_ERROR` — malformed Basic/A3QM payload;
- `QUERY_EXECUTION_ERROR` — valid Basic query unsupported by the current index/runtime;
- `A3QL_SYNTAX_ERROR` — malformed A3QL source;
- `A3QL_EXECUTION_ERROR` — syntactically valid A3QL unsupported by the current index/runtime.

## HTTP mapping

The facade itself does not start a server. A later local transport adapter may map:

- `capabilities()` to `GET /api/capabilities`;
- `execute_basic()` to `POST /api/basic`;
- `execute_advanced()` to `POST /api/advanced`.

Status mapping is stable:

- `200` success, including zero results;
- `400` syntax or input validation failure;
- `422` semantically valid but currently inexecutable query.

## Boundaries

PUB024 does not add authentication, network exposure, dataset upload, result sheets, exports, or a Browser UI. It contains artificial fixtures only and remains suitable for local-first use.
