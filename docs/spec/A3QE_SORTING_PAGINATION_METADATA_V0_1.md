# A3QE Sorting, Pagination and Execution Metadata v0.1

PUB033 adds deterministic paging and sorting to the normalized query path.

## Query fields

Basic A3QM requests may now include:

- `offset`: non-negative integer, default `0`
- `limit`: integer from `1` to `500`
- `sort`: `classname`, `displayName`, or `root`
- `direction`: `asc` or `desc`

## Result contract

Successful Browser responses distinguish:

- `total`: all matches before pagination
- `count`: results in the current page
- `offset` and `limit`: requested page window
- `sort`: effective field and direction
- `execution.durationMs`: measured execution time
- `execution.indexesUsed`: indexes present in the complete execution plan
- `executionPlan`: the explicit PUB032 planner output

Ordering is deterministic and includes stable tie-breakers. Advanced A3QL keeps its current grammar and therefore uses the default paging and sorting values until syntax extensions are introduced.
