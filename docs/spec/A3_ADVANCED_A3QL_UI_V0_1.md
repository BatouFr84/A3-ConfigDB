# A3-ConfigDB Advanced A3QL UI v0.1

PUB026 adds an Advanced search mode beside the validated Basic search UI.

## Contract

The editor accepts only the current A3QL v0.1 grammar:

- `FROM`
- optional `WHERE`
- `AND`
- `LIMIT`
- operators `EQ` and `CONTAINS`

Unsupported SQL-like clauses such as `SELECT`, comparison operators such as `>=`, joins, sorting, and aggregation are rejected.

## Endpoint

`POST /api/advanced`

Request:

```json
{"query":"FROM CfgVehicles WHERE scope EQ 2 LIMIT 100"}
```

Success and error responses use the Browser Backend contract from PUB024.

## UI behavior

- Basic and Advanced modes share the same result table.
- The Advanced editor includes valid artificial-fixture examples.
- Syntax and execution errors are displayed separately from empty successful results.
- The interface remains mobile-first.
- No real Arma 3 data is included.
