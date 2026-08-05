# A3QE v0.1 — Query Engine Baseline

A3QE executes normalized queries over one immutable A3DM snapshot through A3IX indexes.

## Scope

Version 0.1 supports:

- one optional root constraint;
- zero or more filters combined with logical AND;
- `eq` on A3IX exact-index fields;
- `contains` on A3IX property-index paths;
- deterministic ordering by root then classname;
- limits from 1 to 500;
- fail-closed rejection of unknown roots, fields, paths and operators.

## Query model

```python
A3QEQuery(
    root="CfgVehicles",
    filters=(
        A3QEFilter("scope", "eq", 2),
        A3QEFilter("faction", "eq", "A3CDB_TEST_FACTION"),
        A3QEFilter("linkedItems", "contains", "A3CDB_Test_Helmet"),
    ),
    limit=100,
)
```

All filters use AND semantics. Results must satisfy every condition.

## Operator semantics

### `eq`

Exact typed equality through `A3IXExactIndex`.

Text comparisons are case-insensitive. Numeric and boolean values retain their types.

### `contains`

Exact membership among scalar leaves of an indexed array or nested object through `A3IXPropertyIndex`.

In v0.1, `contains` is not a text-substring operator. Text substring search will require a dedicated text index in a later build.

## No silent fallback

A3QE v0.1 does not scan the snapshot when a field is not indexed. An unsupported condition raises `A3QEQueryError` rather than returning incomplete results or triggering an unexpectedly slow full scan.

## Future integration

A3QL and the Basic browser will compile their input into this normalized query model. The execution engine therefore remains independent from user-facing syntax.
