# A3-ConfigDB Public Roadmap

This roadmap follows the snapshot-first, local-first architecture frozen at PUB028. The permanent data boundary remains unchanged: this repository distributes software and artificial fixtures, not extracted Arma 3 configuration databases.

## Completed foundation — PUB001 to PUB028

- [x] Sanitized independent public repository
- [x] AGPL-3.0-or-later licensing and public-data boundary
- [x] Artificial A3DM fixture
- [x] Complete autonomous snapshot doctrine
- [x] A3DM schema and validation baseline
- [x] Immutable snapshot loading API
- [x] A3IX exact index baseline
- [x] A3IX property index baseline
- [x] A3QM normalized query model
- [x] A3QL v0.1 grammar and runtime
- [x] A3QE deterministic query execution
- [x] Browser backend baseline
- [x] Mobile-first Basic search UI
- [x] Advanced A3QL UI
- [x] Basic and Advanced class viewer
- [x] Public CI and Docker validation

## Phase 1 — Local application and dataset lifecycle

### PUB029 — Local HTTP application baseline

- formalize local endpoints;
- stabilize class API behavior;
- improve startup and runtime errors.

### PUB030 — Local dataset loader

- select a local A3DM snapshot;
- load and unload safely;
- display manifest and provenance;
- reject absent, invalid or incompatible datasets clearly.

## Phase 2 — Search completeness and performance

### PUB031 — A3IX text index baseline

- partial case-insensitive search for classname and displayName;
- text search for author, faction and DLC;
- deterministic ordering.

### PUB032 — Hybrid query planner

- choose exact, property or text indexes;
- permit only explicit controlled fallback scans;
- expose the execution plan;
- never return silent partial results.

### PUB033 — Sorting, pagination and metadata

- sort fields and direction;
- offset and limit;
- total matching result count;
- execution duration and index usage.

## Phase 3 — Relations, navigation and exports

### PUB034 — Relations baseline

- class parent and children;
- vehicle to weapons;
- weapon to magazines;
- magazine to ammo;
- validation of missing targets.

### PUB035 — Browser navigation baseline

- clickable parents and relations;
- back/forward history;
- stable local URLs;
- preserve Basic or Advanced view mode.

### PUB036 — Export baseline

- JSON;
- CSV;
- Markdown;
- SQF Array;
- C++-style class output.

## Phase 4 — A3XE extractor foundation

### PUB037 — Extraction contract

Freeze roots, value types, inheritance representation, metadata, addon order, batching, integrity rules and final report format.

### PUB038 — Artificial exporter pipeline

Validate the complete pipeline without Arma 3:

```text
raw artificial export
→ normalization
→ A3DM snapshot
→ validation
→ indexing
→ Browser
```

### PUB039 — First SQF exporter prototype

Implement the first real Arma 3-side export when PC testing is available.

### PUB040 — Integrity, batching and resume

- progress reporting;
- batch export;
- interrupted-export recovery;
- class counts and completeness checks;
- actionable extraction report.

## Phase 5 — Real local datasets and packaging

- representative local dataset performance tests;
- compressed and split A3DM storage;
- persistent index generation;
- offline local-server package;
- self-hosted Docker package;
- upgrade and compatibility policy.

## Deferred components

### A3DIFF

Compare two complete snapshots and report added, removed and modified classes or properties. It is not a storage dependency of A3DM.

### Diagtor

Future standalone dataset diagnostic and compatibility tool. It will be implemented only after A3DM and A3XE are sufficiently stable.

## Target 1.0

A3-ConfigDB 1.0 must let a user:

1. generate a complete dataset from their own Arma 3 installation and active launch preset;
2. retain game version, DLC/addon provenance and observed load order;
3. validate and load the dataset locally;
4. index and search it through Basic and Advanced A3QL modes;
5. inspect local and inherited configuration values;
6. navigate inheritance and key relations;
7. export selected results;
8. keep the real dataset under local control.

## Out of scope for the public repository

- hosting or distributing extracted Arma 3, DLC, cDLC or mod databases;
- bypassing ownership, licensing or access controls;
- requiring cloud storage for normal operation;
- silently returning incomplete search results.