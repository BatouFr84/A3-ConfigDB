# A3QL Runtime v0.1

## Purpose

The A3QL runtime is the public execution boundary between textual A3QL and the indexed A3QE engine.

```text
A3QL source
  -> A3QL parser
  -> A3QM normalized query
  -> A3QE indexed execution
  -> deterministic asset references
```

## Public API

```python
from tools.a3dm_snapshot import A3DMSnapshot
from tools.a3ql_runtime import A3QLRuntime, execute_a3ql

snapshot = A3DMSnapshot.from_file("dataset.json")
runtime = A3QLRuntime(snapshot)
execution = runtime.execute(
    'FROM CfgVehicles WHERE scope EQ 2 LIMIT 100'
)

results = execute_a3ql(
    snapshot,
    'FROM CfgWeapons WHERE scope EQ 2 LIMIT 25',
)
```

`A3QLRuntime.execute()` returns the original source, the snapshot identifier and the immutable deterministic result tuple.

## Error boundary

- `A3QLSyntaxError`: invalid A3QL text or invalid normalized query structure.
- `A3QLExecutionError`: the parsed query cannot be executed by A3QE, for example an unknown root or a non-indexed field.
- An empty result set is a successful execution, not an error.

## v0.1 guarantees

- Basic and Advanced clients can converge on the same A3QM/A3QE execution path.
- No silent full-dataset fallback scan is performed.
- Result ordering and limits are controlled by A3QE.
- The runtime contains no web, UI or export-specific behavior.

## Deferred

- text-substring index and operator;
- OR, NOT and parentheses;
- sorting and projections;
- query timing and execution plans;
- Browser/API integration.
