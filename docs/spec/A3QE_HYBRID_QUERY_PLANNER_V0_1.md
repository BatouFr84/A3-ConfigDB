# A3QE Hybrid Query Planner v0.1

PUB032 makes index selection explicit and observable.

## Routes

- `EQ` uses A3IX Exact.
- `CONTAINS` on `classname`, `displayName`, `author`, `faction`, or `dlc` uses A3IX Text.
- `CONTAINS` on declared collection properties uses A3IX Property.

A query with no complete route is rejected. The planner never substitutes a partial scan or silently returns incomplete results.

## Ordering

Each root constraint and filter is estimated from its selected index. Steps are ordered from the smallest estimated candidate set to the largest, with deterministic tie-breaking. Final results remain sorted by root and classname.

## Response metadata

Successful Browser Backend responses expose `executionPlan` with:

- selected index per step;
- estimated match count;
- original filter ordinal;
- `complete: true`;
- `fallback: null`.

Capabilities expose the available planner indexes and the permanent no-silent-fallback contract.

## Limits

This baseline does not yet provide cost models, persisted statistics, adaptive planning, range indexes, or controlled scans. Those features require explicit future contracts and may not weaken result completeness.
