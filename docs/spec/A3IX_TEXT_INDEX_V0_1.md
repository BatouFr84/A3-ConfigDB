# A3IX Text Index v0.1

## Status

Introduced by `PUB031 — A3IX Text Index baseline`.

## Purpose

A3IX Text Index provides deterministic, case-insensitive substring lookup for selected scalar text fields without scanning the full snapshot during each query.

## Indexed fields

- `classname`
- `displayName`
- `author`
- `faction`
- `dlc`

The list is explicit and versioned. Unsupported fields are rejected rather than silently scanned.

## Query semantics

For the indexed fields, A3QE routes the existing `contains` operator to A3IX Text Index.

Example:

```a3ql
FROM CfgWeapons
WHERE classname CONTAINS "rif"
LIMIT 10
```

Matching is:

- case-insensitive through Unicode `casefold` normalization;
- substring-based;
- optionally restricted to one root;
- sorted deterministically by root and classname;
- complete for the selected indexed field.

## Separation from property contains

`contains` keeps its existing collection-membership meaning for non-text fields handled by A3IX Property Index, such as `linkedItems`.

Therefore:

- `displayName CONTAINS "rifle"` means text substring search;
- `linkedItems CONTAINS "A3CDB_Test_Helmet"` means collection membership.

No incomplete fallback is performed. A field unsupported by both index families produces a query execution error.

## Capabilities

The Browser Backend exposes the active list as:

```json
{
  "textIndexedFields": [
    "classname",
    "displayName",
    "author",
    "faction",
    "dlc"
  ]
}
```

## Limitations

Version 0.1 does not provide tokenization, stemming, fuzzy matching, relevance ranking, prefix trees, persisted index files, or language-specific normalization. Index construction currently occurs in memory when a snapshot is loaded.
