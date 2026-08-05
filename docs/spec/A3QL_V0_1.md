# A3QL v0.1

A3QL is the human-readable query language for A3-ConfigDB. Version 0.1 is deliberately small and maps directly to the normalized A3QM query model.

## Grammar

```text
query       := FROM root [WHERE condition (AND condition)*] [LIMIT integer]
condition   := field operator value
operator    := EQ | CONTAINS
value       := quoted-string | integer | float | true | false
root        := identifier
field       := identifier
```

Keywords are case-insensitive. Root names, field names and string values preserve their original case.

## Examples

```sql
FROM CfgVehicles
```

```sql
FROM CfgVehicles
WHERE scope EQ 2
LIMIT 100
```

```sql
FROM CfgVehicles
WHERE scope EQ 2
AND linkedItems CONTAINS "A3CDB_Test_Helmet"
LIMIT 50
```

## Semantics

- `EQ` maps to the A3IX exact index.
- `CONTAINS` maps to the A3IX property index and means exact scalar membership inside an indexed list or nested structure.
- Multiple conditions are combined with logical `AND`.
- `LIMIT` defaults to 100 and must be between 1 and 500.
- Bare string values are rejected; strings must be quoted.
- Unsupported operators and trailing tokens are rejected.
- The parser returns an immutable `A3QMQuery`, not an executable result.

## Out of scope for v0.1

- `OR` and `NOT`
- parentheses
- comparison operators such as `GT`, `LT`, `GTE`, `LTE`
- substring text search
- ordering and projection
- comments
- multiple datasets or profiles in one query

These features require explicit later versions and must not be accepted silently by a v0.1 parser.
