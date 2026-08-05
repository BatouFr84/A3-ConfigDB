# Public Project Status

## Current checkpoint

`PUB028 — Complete project recap and architecture checkpoint`

PUB028 is a documentary consolidation build. Its code baseline is the validated `PUB027` class viewer checkpoint.

## Validated end-to-end foundation

The public repository currently provides:

- a sanitized AGPL-3.0-or-later repository containing artificial data only;
- A3DM complete snapshot schema and fail-closed validation;
- immutable snapshot loading and inherited-property resolution;
- A3IX exact and nested-property index baselines;
- A3QE deterministic multi-filter execution;
- A3QM normalized query model;
- A3QL v0.1 parser and runtime;
- Browser backend with stable JSON success/error envelopes;
- mobile-first Basic and Advanced search interfaces;
- Basic and C++-style Advanced class sheets;
- public Python, compilation and Docker CI validation.

## Current functional chain

```text
Artificial A3DM snapshot
→ validation
→ immutable loading
→ exact/property indexing
→ Basic or A3QL query
→ A3QE execution
→ result table
→ Basic or Advanced class viewer
```

## Explicit limitations

The public preview does not yet include:

- extraction from a local Arma 3 installation;
- user-selected local dataset loading;
- compressed or split snapshot storage;
- persistent or text indexes;
- a hybrid query planner;
- sorting and pagination;
- navigable inheritance and relation graphs;
- unified exports;
- offline desktop packaging.

No real Arma 3, DLC, cDLC or mod configuration data is distributed.

## Architectural doctrine

- One extraction is one complete autonomous final snapshot.
- Addon order is recorded as provenance metadata.
- Differential storage is not part of the A3DM core; future comparison belongs to A3DIFF.
- A3XE is the central future extractor and dataset builder.
- `Diagtor` is reserved for a later dataset diagnostic tool.
- Unsupported execution must fail explicitly; silent incomplete results are forbidden.

## Next planned sequence

```text
PUB029  Local HTTP application baseline
PUB030  Local dataset loader
PUB031  A3IX text index baseline
PUB032  Hybrid query planner
PUB033  Sorting, pagination and execution metadata
PUB034  Relations baseline
PUB035  Browser navigation baseline
PUB036  Export baseline
PUB037+ A3XE extraction foundation
```

See [`docs/checkpoints/PUB028_ARCHITECTURE_CHECKPOINT.md`](docs/checkpoints/PUB028_ARCHITECTURE_CHECKPOINT.md) for the complete architecture and [`ROADMAP.md`](ROADMAP.md) for the updated route to 1.0.

## Repository boundary

The historical development repository remains private under `A3-ConfigDB-private`. This public repository has an independent sanitized history and must remain free of extracted real game configuration databases.