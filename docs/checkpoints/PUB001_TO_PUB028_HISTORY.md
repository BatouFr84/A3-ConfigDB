# Public Build History — PUB001 to PUB028

This history records the major public development sequence. Hotfix suffixes are included where they materially changed the validated checkpoint.

## PUB001–PUB009 — Public staging and repository boundary

The project was separated from the historical private repository, sanitized for publication, limited to artificial fixtures, documented, licensed and prepared for independent public validation. The public Docker demonstration and repository-boundary checks were established during this sequence.

## PUB010–PUB012A — Publication gates

The repository passed zero-data-exposure, license, manifest, external runtime, Docker and final publication checks. PUB012A corrected a document-validator false positive without weakening the public-data boundary.

## PUB013 — Cleanup and roadmap baseline

The initial public checkpoint consolidated the sanitized repository, status documents and first public roadmap.

## PUB014–PUB015 — A3DM design exploration

The dataset model and inheritance concepts were explored. The project initially considered differential profiles, then identified the practical reality that most users will export one complete launch preset rather than many individual addon layers.

## PUB016 / PUB016A — A3DM snapshot-first pivot

PUB016 implemented a differential-profile validator prototype. PUB016A deliberately replaced that core model with a complete autonomous snapshot doctrine:

- one extraction equals one final observed configuration snapshot;
- addon order is provenance metadata;
- Arma 3 has already resolved config priority;
- differential comparison is deferred to A3DIFF.

## PUB017 / PUB017A / PUB017B — Immutable snapshot loading API

The project gained a validated read-only A3DM loading boundary, root and class access, and inherited-property resolution. Hotfixes aligned the runtime API and tests with the actual snapshot fixture contract.

## PUB018 — A3IX exact index baseline

Exact, case-insensitive indexing was added for common fields such as classname, root, displayName, parent, scope, author, DLC and faction.

## PUB019 — A3IX property index baseline

Exact membership indexing was added for nested and array properties such as linkedItems, weapons, magazines, turrets and transportItems.

## PUB020 — A3QE query engine v0.1

A deterministic multi-filter AND engine was added. It combines validated indexes and rejects unsupported fields or operators instead of silently scanning or returning partial results.

## PUB021 — A3QM normalized query model

A single immutable query contract was introduced for Basic UI, A3QL, APIs, exports and A3QE.

## PUB022 — A3QL grammar v0.1

The first language grammar was validated with:

- `FROM`;
- optional `WHERE`;
- `AND`;
- `LIMIT`;
- `EQ`;
- `CONTAINS`.

## PUB023 — A3QL runtime integration

The full chain became executable:

```text
A3QL → A3QM → A3QE → A3IX → A3DM snapshot
```

Syntax and execution failures remained distinct.

## PUB024 / PUB024A — Browser backend baseline

A transport-neutral Browser facade was added for Basic and Advanced requests with stable JSON success/error envelopes. PUB024A corrected the runtime limit contract.

## PUB025 — Basic Search UI baseline

The public demo gained a mobile-first Basic query builder with dynamic roots, filters, limits, result states and a structured result table.

## PUB026 — Advanced A3QL UI

The public demo gained a separate Advanced editor using the validated A3QL grammar, examples, error display and the same result table as Basic mode.

## PUB027 — Basic and Advanced class viewer

Clickable results and a class API were added. The Browser can display a digestible Basic sheet and an Advanced C++-style representation with local and resolved inherited properties.

## PUB028 — Architecture checkpoint

PUB028 consolidates the actual state of the project, removes obsolete differential-profile roadmap assumptions, records the module boundaries and defines the route toward local dataset loading, text indexing, relations, exports and A3XE.

## Validated checkpoint at the opening of PUB028

```text
PUB027
Head: 6f45e23e245ec153221d9791fd53e3f395e30266
CI: PASS
```

PUB028 itself remains unvalidated until its workflow passes.