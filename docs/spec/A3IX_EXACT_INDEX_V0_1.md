# A3IX v0.1 — Exact index baseline

Status: public prototype.

A3IX v0.1 builds an immutable in-memory exact-match index from one validated `A3DMSnapshot`.

## Indexed fields

- `classname`
- `root`
- `displayName`
- `parent`
- `scope`
- `author`
- `dlc`
- `faction`

`displayName`, `scope`, `author`, `dlc` and `faction` are indexed from the fully resolved Arma-style property view, so inherited values remain searchable.

## Matching rules

Text matching is exact after Unicode case folding. Numeric and boolean values retain their type. Missing or unsupported complex values are not indexed.

Examples:

```python
index.exact("classname", "A3CDB_Test_Soldier")
index.exact("displayName", "A3CDB Test Rifleman")
index.exact("scope", 2, root="CfgVehicles")
```

Each result is an immutable `A3IXAssetRef(root, classname)`.

## Guarantees

- the source snapshot remains immutable;
- result order is deterministic;
- unknown indexed values return an empty tuple;
- unknown fields fail explicitly;
- no fallback scan is performed in this baseline;
- no result can silently claim completeness for an unindexed field.

## Deferred work

Substring search, token search, nested-property indexing, persistent on-disk indexes, memory budgeting and hybrid fallback belong to later A3IX builds.
