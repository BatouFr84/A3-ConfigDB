# A3-ConfigDB Public Roadmap

This roadmap follows the snapshot-first, local-first architecture confirmed by PUB044. The public repository distributes software, schemas and artificial fixtures, not extracted real game databases.

## Completed through PUB043

### Public foundation

- [x] Sanitized independent public repository
- [x] AGPL-3.0-or-later licensing
- [x] Artificial-data-only public boundary
- [x] Public CI, compilation and Docker validation

### A3DM and query stack

- [x] Autonomous snapshot doctrine
- [x] A3DM schema and fail-closed validation
- [x] Immutable snapshot loader
- [x] A3IX exact, property and text indexes
- [x] A3QM normalized query model
- [x] A3QE deterministic execution
- [x] A3QL v0.1
- [x] Hybrid query planner
- [x] Sorting, pagination and execution metadata

### Local application and Browser

- [x] Local HTTP application
- [x] Local dataset loader
- [x] Mobile-first Basic and Advanced modes
- [x] Basic and C++-style class sheets
- [x] Parent, children and known native relations
- [x] Browser history and stable class URLs
- [x] JSON, CSV, Markdown, SQF and C++-style exports

### A3XE foundation

- [x] Extraction contract
- [x] Artificial exporter pipeline
- [x] Controlled SQF capture prototype
- [x] Integrity and resume primitives
- [x] Complete inheritance derivation
- [x] Local/resolved/source property maps
- [x] Native relation derivation

## PUB044 — Full project audit

- [x] Record actual versus expected behavior
- [x] Identify real implementation gaps
- [x] Re-estimate progress to 1.0
- [x] Freeze the route to the first controlled real extraction

See `docs/checkpoints/PUB044_FULL_PROJECT_AUDIT.md`.

## Next extraction sequence

### PUB045 — Multi-root Extraction Baseline

- accept multiple roots in one extraction run;
- preserve deterministic root and class ordering;
- aggregate counts and diagnostics;
- validate each root independently;
- emit one coherent A3DM snapshot.

### PUB046 — First Controlled Real Arma 3 Test Pack

- provide exact PC execution instructions;
- run one small real extraction;
- collect capture and RPT markers;
- convert through the public pipeline;
- document engine-specific failures.

### PUB047 — Typed Property Coverage

- extend beyond four controlled scalar properties;
- support strings, numbers and arrays first;
- preserve exact supported types;
- report unsupported config values explicitly.

### PUB048 — SQF Batching and Checkpoints

- bounded capture batches;
- persistent progress state;
- interrupted-run recovery;
- strict environment fingerprint checks;
- final atomic publication.

### PUB049 — First Partial Vanilla Snapshot

- selected useful roots;
- controlled property coverage;
- Browser loading and query validation;
- size, load-time and memory measurements.

### PUB050+ — Full Vanilla Candidate

- broaden roots and property coverage;
- complete known relations;
- persistent indexes and storage optimization;
- user-friendly local packaging;
- legal review before any optional prebuilt dataset publication.

## Later application work

- desktop-native dataset selection;
- live dataset switching;
- compressed or split A3DM storage;
- persistent index generation;
- saved queries and export presets;
- accessibility and mobile usability pass on real data;
- offline desktop and self-hosted packages.

## Deferred components

### A3DIFF

Compare two complete autonomous snapshots. It is not a storage dependency of A3DM.

### Diagtor

Diagnose real snapshots, missing targets, suspicious types and load-order conflicts. Development starts only after representative real datasets exist.

## Target 1.0

A3-ConfigDB 1.0 must let a user:

1. generate a complete dataset from their own Arma 3 installation and active preset;
2. preserve game version, addon provenance and observed load order;
3. validate and load the dataset locally;
4. search through Basic and Advanced A3QL modes;
5. inspect local and inherited values;
6. navigate inheritance and key relations;
7. export complete selected results;
8. keep real extracted data under local control.

## Out of scope for the public repository

- silently returning incomplete results;
- bypassing ownership or access controls;
- requiring cloud storage for normal operation;
- distributing extracted Arma 3, DLC, cDLC or mod databases without a separately established legal basis.