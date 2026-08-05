# PUB028 — Complete Architecture Checkpoint

## Status

This document freezes the public architecture after the validated `PUB027` checkpoint. The repository still contains artificial `A3CDB_Test_*` data only.

## Product definition

A3-ConfigDB is a local-first Arma 3 configuration exploration platform. Users will generate a complete snapshot from their own installation and launch preset, load it locally, index it, query it, inspect class inheritance and relations, and export selected results.

The public repository distributes the software, schemas, documentation and artificial fixtures. It does not distribute extracted Arma 3, DLC, cDLC or mod configuration databases.

## Core decisions

1. One extraction represents one complete final snapshot of the configuration observed by Arma 3.
2. Arma 3 has already resolved addon priority before extraction. The recorded addon order is provenance metadata, not a reconstruction instruction.
3. Differential storage is not the A3DM core. Future comparisons belong to `A3DIFF`.
4. A3-ConfigDB is local-first. Real datasets remain under the user’s control.
5. A3XE is the central future component because dataset quality determines every downstream result.
6. Basic and Advanced searches use the same normalized query and execution chain.
7. No silent partial result is acceptable. Unsupported queries must fail explicitly.
8. `Diagtor` is the reserved name for the future dataset diagnostic tool, but it remains out of the current implementation scope.

## Validated architecture

```text
A3XE (future extractor)
        |
        v
A3DM complete snapshot
        |
        v
A3DMSnapshot immutable loading API
        |
        +--> A3IX exact index
        +--> A3IX property index
        |
        v
A3QE execution engine
        ^
        |
A3QM normalized query model
        ^
        |
   +----+----+
   |         |
Basic UI   A3QL parser/runtime
   |         |
   +----+----+
        |
Browser backend and local HTTP facade
        |
        v
Basic/Advanced Browser and class viewer
```

## Module state

| Module | State at PUB028 | Current capability | Main missing work |
|---|---|---|---|
| Public repository boundary | Validated | Sanitized AGPL repository, artificial fixtures only | Ongoing audits |
| A3DM | Baseline validated | Complete autonomous snapshot, manifest, provenance, schema validation | Compression, checksums, compatibility evolution |
| Snapshot API | Baseline validated | Immutable load, root/class access, inherited property resolution | Split/compressed storage support |
| A3IX exact | Baseline validated | Exact lookup on common fields | Persistence and scale testing |
| A3IX property | Baseline validated | Exact membership in nested arrays/objects | Broader property coverage |
| A3IX text | Not started | — | Fast substring/token search |
| A3QM | v0.1 validated | Stable normalized Basic/Advanced query contract | Future operators and sorting |
| A3QL | v0.1 validated | `FROM`, `WHERE`, `AND`, `LIMIT`, `EQ`, `CONTAINS` | `OR`, comparisons, sorting, projections, help system |
| A3QE | v0.1 validated | Deterministic multi-filter AND execution using indexes | Query planning, pagination, diagnostics |
| Browser backend | Baseline validated | Basic/A3QL execution, stable JSON responses, metadata and errors | Local dataset lifecycle and richer class APIs |
| Basic UI | Baseline validated | Mobile-first query builder and result table | Rich field metadata and saved queries |
| Advanced UI | Baseline validated | A3QL editor, examples and error display | Formatting, help and history |
| Class viewer | Baseline validated | Basic sheet and C++-style Advanced sheet | Parent navigation, relations, permanent URLs |
| A3XE | Not started | Contract concept only | Arma-side extraction, normalization, report, recovery |
| A3DIFF | Deferred | Design intent only | Snapshot comparison engine |
| Diagtor | Deferred | Name and role reserved | Dataset integrity and compatibility diagnostics |

## Current end-to-end capability

```text
Artificial A3DM fixture
→ validation
→ immutable loading
→ exact/property indexing
→ normalized Basic or A3QL query
→ A3QE execution
→ Browser JSON response
→ result table
→ Basic or Advanced class sheet
```

This chain is functional and covered by public CI. It is not yet a complete end-user product because it cannot load a user-selected local dataset and cannot extract real data from Arma 3.

## Current limitations

- Artificial fixture only.
- No local dataset selector or lifecycle.
- No A3XE extractor.
- No compressed multi-file datasets.
- No persistent indexes.
- No substring text index.
- No hybrid query planner.
- No sorting, offset or total-count pagination.
- No outgoing or incoming relation graph.
- Parent and referenced classes are not yet navigable.
- No unified JSON, CSV, Markdown or SQF export.
- No offline desktop package.

## Stability rules

The following contracts are considered stable baselines, not immutable final standards:

- A3DM snapshot-first doctrine.
- Immutable snapshot access boundary.
- A3QM query envelope: `root`, `filters`, `limit`.
- Browser success/error envelope.
- Explicit distinction between syntax, validation and execution errors.
- Artificial-data-only public repository boundary.

Any incompatible change must be versioned and documented. Backward compatibility must not be broken silently.

## Immediate roadmap

### PUB029 — Local HTTP application baseline

Formalize the local application endpoints and class API around the validated backend.

### PUB030 — Local dataset loader

Select, load, unload and inspect a user-provided A3DM snapshot without relying on the bundled fixture.

### PUB031 — A3IX text index baseline

Fast case-insensitive partial search for classname, displayName, author, faction and DLC.

### PUB032 — Hybrid query planner

Choose exact, property or text indexes and permit only explicit controlled fallback execution.

### PUB033 — Sorting, pagination and execution metadata

Add sort, offset, total, duration and index-plan information.

### PUB034–PUB036 — Relations, navigation and exports

Implement parent/child and weapon/magazine/ammo relations, navigable sheets, and initial export formats.

### PUB037–PUB040 — A3XE foundation

Freeze the extraction contract, validate an artificial exporter pipeline, implement the first SQF prototype when PC testing is available, then add integrity reporting and resume support.

## Target 1.0

A3-ConfigDB 1.0 must allow a user to:

1. extract a complete dataset from their own Arma 3 installation and active launch preset;
2. obtain a clear extraction report including game version and addon order;
3. load and validate the dataset locally;
4. build required indexes locally;
5. search in Basic or A3QL mode;
6. inspect resolved and local configuration values;
7. navigate inheritance and key relations;
8. export selected results;
9. perform all of this without uploading the real dataset to a public service.

## Checkpoint conclusion

PUB028 closes the first public foundation cycle. The project has a coherent working query and browsing stack, but the decisive remaining work is the local dataset lifecycle and A3XE extraction pipeline. Future builds must prioritize reliability, provenance and complete results over decorative features.