# A3QM v0.1 — Normalized Query Model

## Purpose

A3QM is the single normalized query contract shared by the Basic interface, the future A3QL parser, the web API, exports and A3QE.

A producer may use any user-facing syntax, but it must normalize the request to this structure before execution.

## Canonical shape

```json
{
  "root": "CfgVehicles",
  "filters": [
    {
      "field": "scope",
      "operator": "eq",
      "value": 2
    },
    {
      "field": "linkedItems",
      "operator": "contains",
      "value": "A3CDB_Test_Helmet"
    }
  ],
  "limit": 100
}
```

## Rules

- `root` is a non-empty string or `null`.
- `filters` is an ordered array of filter objects.
- each filter has exactly `field`, `operator` and `value`;
- operator names are normalized to lowercase;
- `limit` defaults to 100 and must be between 1 and 500;
- unknown fields are rejected rather than ignored;
- A3QM validates structure, while A3QE validates whether a root, field or operator is executable against the loaded snapshot and indexes.

## Execution boundary

`normalize_query(payload)` returns an immutable `A3QMQuery`.

`A3QMQuery.to_a3qe()` converts the normalized model to the current A3QE execution contract. The Basic UI and future A3QL parser must not construct A3QE filters independently.

## v0.1 scope

The model supports AND-combined filters only because that is the current A3QE capability. OR groups, sorting, projections, pagination cursors and text-substring operators are deliberately deferred.
