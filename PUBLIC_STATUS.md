# Public Project Status

## Current checkpoint

`PUB044 — Full Project Checkpoint and Technical Audit`

PUB044 consolidates the validated implementation through `PUB043` and defines the controlled route to the first real Arma 3 dataset.

## Current functional chain

```text
Controlled SQF capture prototype
→ capture validation
→ inheritance reconstruction
→ resolved properties
→ native relations
→ A3DM snapshot
→ local dataset loader
→ A3IX indexes
→ A3QE / A3QL queries
→ Browser navigation and exports
```

## Stable or functional baselines

- sanitized AGPL-3.0-or-later public repository with artificial fixtures only;
- A3DM snapshot schema, validator and immutable loader;
- A3IX exact, property and text indexes;
- A3QM, A3QE and A3QL v0.1;
- hybrid query planner, sorting, pagination and execution metadata;
- local HTTP application and local dataset loading;
- mobile-first Basic and Advanced Browser;
- class sheets, inheritance and relation navigation;
- JSON, CSV, Markdown, SQF and C++-style exports;
- A3XE extraction contract and artificial exporter;
- controlled `CfgWeapons` SQF capture prototype;
- integrity/resume primitives;
- complete inheritance, resolved-property and native-relation derivation.

## Main unfinished area

The Python and Browser architecture is ahead of the real Arma-side extractor.

Still required:

- multi-root SQF capture;
- broader typed property extraction;
- batching and real SQF checkpoints;
- real addon/load-order provenance acquisition;
- first controlled PC extraction;
- first partial then complete Vanilla snapshot;
- large-dataset performance and packaging work.

## Architectural doctrine

- One extraction is one complete autonomous final snapshot.
- The final state visible in `configFile` is authoritative.
- Addon order is recorded as provenance, not treated as universal.
- Differential comparison belongs to future A3DIFF, not A3DM storage.
- Unsupported or incomplete execution must fail explicitly.
- `Diagtor` remains deferred until representative real datasets exist.

## Immediate sequence

```text
PUB045  Multi-root extraction baseline
PUB046  First controlled real Arma 3 PC test
PUB047  Typed property coverage
PUB048  SQF batching and checkpoints
PUB049  First partial Vanilla snapshot
PUB050+ Full Vanilla candidate and optimization
```

See [`docs/checkpoints/PUB044_FULL_PROJECT_AUDIT.md`](docs/checkpoints/PUB044_FULL_PROJECT_AUDIT.md) for the complete mobile-readable audit.

## Repository boundary

The historical development repository remains private under `A3-ConfigDB-private`. The public `A3-ConfigDB` repository distributes software, schemas and artificial fixtures, not extracted real Arma 3, DLC, cDLC or mod databases.