# PUB044 — Full Project Checkpoint and Technical Audit

> Mobile-first reading order: read sections 1, 2, 3 and 12 first. The remaining sections are the technical reference.

## 1. Executive status

A3-ConfigDB is no longer a concept prototype. The public repository now contains a coherent local-first application stack and the first controlled A3XE extraction chain.

Current validated checkpoint before this audit: `PUB043`.

Current functional chain:

```text
Arma 3 controlled SQF capture prototype
→ capture validation
→ inheritance reconstruction
→ resolved-property derivation
→ native-relation derivation
→ A3DM snapshot validation
→ local dataset loading
→ A3IX indexing
→ A3QE / A3QL queries
→ Browser results and class sheets
→ relation navigation
→ exports
```

What is genuinely complete today:

- public/private repository separation;
- artificial-data-only public boundary;
- A3DM v0.1 baseline and fail-closed validator;
- immutable snapshot loading;
- exact, property and text indexes;
- deterministic query engine and A3QL v0.1;
- local HTTP application and dataset loading;
- Basic and Advanced Browser modes;
- class sheets, relations, history and exports;
- A3XE contract, artificial exporter, controlled SQF prototype;
- integrity/resume primitives;
- inheritance, resolved properties and native-relation derivation.

What is not complete:

- real multi-root capture from Arma 3;
- broad property extraction;
- real addon/load-order acquisition;
- batch/checkpoint writing from SQF;
- a representative full Vanilla snapshot;
- large-volume performance validation;
- desktop packaging;
- Diagtor;
- legal clearance for distributing optional prebuilt real datasets.

## 2. Progress dashboard

Percentages are engineering estimates, not marketing claims.

| Domain | State | Estimate |
|---|---|---:|
| Public repository and data boundary | Stable | 95% |
| A3DM snapshot format | Stable baseline | 80% |
| Validators and integrity | Functional baseline | 80% |
| A3IX indexes | Functional baseline | 75% |
| A3QE / A3QM / A3QL | Functional baseline | 75% |
| Local HTTP application | Functional baseline | 75% |
| Browser Basic / Advanced | Functional baseline | 75% |
| Relations, navigation and exports | Functional baseline | 70% |
| A3XE architecture | Solid | 80% |
| A3XE real SQF extraction | Controlled prototype | 30% |
| Multi-root extraction | Not implemented | 10% |
| Real Vanilla dataset production | Not started | 0% |
| Large dataset performance work | Not started | 5% |
| Offline desktop packaging | Not started | 0% |
| Diagtor | Reserved only | 0% |
| Overall road to usable 1.0 | In progress | 58% |

The project is further advanced as a software architecture than as a real Arma 3 extractor. That imbalance is deliberate and now needs to be corrected by real extraction work.

## 3. What the user should expect today

### 3.1 Browser behavior

With a valid A3DM snapshot loaded, the Browser can:

- display dataset provenance and manifest information;
- search through Basic filters;
- execute A3QL queries in Advanced mode;
- use exact, nested-property and text indexes;
- expose the query plan, duration and indexes used;
- sort and paginate results;
- open a Basic or Advanced class sheet;
- display local and inherited values;
- navigate parent, children and known relations;
- keep class/view state in the URL and browser history;
- export complete results or one class sheet.

The Browser must refuse incomplete exports when only one paginated page is loaded.

### 3.2 Dataset behavior

A dataset is one autonomous final snapshot. It is not a differential overlay stack.

The snapshot records the environment that produced it, including observed addon order. A user who extracts `Arma 3 + CBA + ACE + RHS` receives the final configuration state produced by that exact loaded preset.

Changing mod order can change the final snapshot. Therefore addon order is provenance, not a universal priority table.

### 3.3 Failure behavior

The core doctrine is fail-closed:

- invalid snapshots are rejected;
- missing datasets return an explicit unavailable state;
- unsupported query execution cannot return partial results silently;
- missing relation targets remain visible and marked missing;
- unsupported extraction values must be reported, not converted silently;
- resume is rejected when the environment fingerprint changes.

## 4. Repository architecture

### Public repository

Repository: `A3-ConfigDB`.

Purpose:

- public source code;
- schemas and specifications;
- artificial fixtures;
- CI and Docker validation;
- no distributed extracted real game database.

### Private repository

Repository: `A3-ConfigDB-private`.

Purpose:

- historical/private development material;
- private experiments or data that must not cross the public boundary;
- future internal staging when necessary.

The public repository must never regain private history through a merge, force-push or copied extracted dataset.

## 5. Component-by-component audit

### 5.1 A3DM — snapshot model

Implemented:

- manifest and snapshot separation;
- roots and classes;
- direct parent storage;
- local properties;
- strict validation;
- immutable loading API;
- canonical snapshot identity fields;
- artificial/real-data boundary flags.

Expected behavior:

- preserve primitive JSON-compatible types;
- preserve direct inheritance rather than flattening it destructively;
- validate parents and cycles;
- allow resolved properties to be derived reproducibly.

Remaining:

- versioned migration policy;
- compressed/split storage;
- optional persistent indexes;
- proven behavior on full-size real datasets.

### 5.2 A3IX — indexes

Implemented:

- exact index;
- nested-property index;
- text index for `classname`, `displayName`, `author`, `faction`, `dlc`;
- deterministic candidate ordering;
- planner integration.

Expected behavior:

- text `CONTAINS` and collection membership are distinct operations;
- planner selects exact/property/text routes explicitly;
- incomplete fallback is forbidden.

Remaining:

- persistent on-disk indexes;
- tokenizer and multi-word search;
- relevance scoring or fuzzy search;
- memory/performance profiling on large datasets.

### 5.3 A3QE / A3QM / A3QL

Implemented:

- normalized query model;
- Basic query execution;
- A3QL v0.1 parser/runtime;
- multi-filter intersections;
- hybrid query planner;
- stable sorting;
- offset/limit pagination;
- `count` versus `total` distinction;
- execution-plan and duration metadata.

Remaining:

- `ORDER BY` and `OFFSET` syntax inside A3QL itself;
- richer boolean groups;
- aggregation;
- saved queries;
- large-volume optimization.

### 5.4 Local application

Implemented:

- local HTTP server;
- application/backend separation;
- health and dataset state;
- dataset selected through local startup configuration;
- graceful no-dataset state;
- stable JSON success/error envelopes.

Remaining:

- Browser file picker or desktop-native selection;
- live dataset switching;
- last-used dataset persistence;
- multiple loaded datasets;
- desktop launcher and installer.

### 5.5 Browser

Implemented:

- mobile-first Basic mode;
- Advanced A3QL mode;
- result table;
- Basic and C++-style class views;
- clickable parent/children/native relations;
- missing-target display;
- internal and browser back/forward history;
- stable query-string class URLs;
- JSON, CSV, Markdown, SQF and C++-style exports.

Remaining:

- dataset file selection UI;
- breadcrumb and richer navigation context;
- visual relation graph;
- improved mobile tables for very wide property sets;
- saved searches/export presets;
- accessibility and usability pass on real data.

### 5.6 A3XE — extraction system

Implemented:

- extraction contract;
- artificial exporter proving the full pipeline;
- controlled SQF capture prototype;
- current controlled root: `CfgWeapons`;
- current controlled properties: `displayName`, `scope`, `author`, `dlc`;
- SQF capture converter;
- integrity fingerprint and resume-state primitives;
- complete inheritance-chain derivation;
- local/resolved/source property maps;
- native relation derivation engine;
- explicit diagnostics and atomic output writing.

Important limitation:

The current SQF script has not yet proven a complete multi-root real extraction. The Python side is substantially ahead of the Arma-side acquisition layer.

Remaining:

- multi-root capture;
- batch capture and real SQF checkpoints;
- broad typed property enumeration;
- array and nested-class handling from config space;
- addon and DLC provenance acquisition;
- relation-bearing properties in real captures;
- full end-to-end PC tests;
- first partial and then complete Vanilla snapshot.

## 6. Inheritance and overwrite doctrine

A3-ConfigDB follows Arma 3's final loaded configuration state.

For one class:

```text
base class local values
→ child local overrides
→ later loaded addon configuration effects already present in configFile
→ final resolved value
```

A3XE does not need to recreate every historical patch operation. It extracts the final state visible in the running game and records the observed environment/load order that produced it.

Stored data:

- direct parent;
- local values;
- derived resolved values;
- source class for each resolved value.

For a relation inherited from a parent, `sourceClass` identifies the class that supplied the property.

## 7. Relation model

Current known relations:

```text
Class → parent
Parent → children
CfgVehicles.weapons → CfgWeapons
CfgWeapons.magazines → CfgMagazines
CfgMagazines.ammo → CfgAmmo
```

Each target carries:

- target root;
- target classname;
- existence flag;
- source class.

Missing targets are valid diagnostics, not invisible deletions.

Future relation work:

- nested turret weapons and magazines;
- muzzle/mode structures;
- compatible items and weapon slots;
- faction/crew links;
- model/config references where useful;
- reverse relation indexes at dataset-build time.

## 8. Integrity and resume

Implemented primitives:

- canonical JSON;
- SHA-256 digest;
- atomic file replacement;
- monotonic progress state;
- environment fingerprint;
- rejection when game build, addon order, roots or extraction modes change;
- final A3DM validation;
- class-count and inheritance integrity checks.

Missing operational integration:

- SQF must emit batches and checkpoint data;
- Python must assemble those batches into one final run;
- interruption and restart must be tested in a real long extraction;
- temporary files and completed files need a user-facing cleanup policy.

## 9. Tests and confidence

Current CI validates:

- public repository boundary and licensing;
- artificial fixture validity;
- Python unit tests;
- Python compilation;
- Docker build;
- Browser contract checks;
- extractor converters and derived metadata using artificial representative captures.

What CI cannot prove:

- SQF execution correctness inside the current Arma 3 build;
- clipboard/RPT size limits on large captures;
- performance and memory usage with tens of thousands of classes;
- exact behavior of uncommon config value types;
- mod-specific malformed or unusual configurations;
- full load-order metadata acquisition.

Therefore the next phase requires user-operated PC tests, not more artificial-only confidence.

## 10. Data, legal and distribution position

Current safe position:

- public code and artificial fixtures are distributed;
- users may generate local snapshots from installations and presets they can access;
- no real Arma 3, DLC, cDLC or mod database is currently shipped from this repository.

Open legal question:

Whether an optional prebuilt Vanilla snapshot can be distributed should be reviewed separately before publication. Classnames and factual configuration values may be publicly observable, but a compiled bulk database can still raise licensing, database-right, contractual or publisher-policy questions depending on jurisdiction and content. No permission should be assumed.

Pragmatic policy until reviewed:

- keep real snapshots local;
- publish the extractor and schemas;
- do not bundle real game data in releases;
- document provenance and user responsibility;
- seek permission or legal review before distributing a prebuilt snapshot.

## 11. Diagtor

`Diagtor` remains reserved and intentionally unimplemented.

Future role:

- inspect one snapshot for structural and semantic problems;
- report missing targets, suspicious types and broken relation chains;
- compare snapshot capabilities with Browser requirements;
- diagnose mod/load-order conflicts;
- produce a readable compatibility report.

Diagtor should begin only after A3XE can produce representative real datasets. Building it now would diagnose artificial assumptions rather than real problems.

## 12. Ordered plan from this checkpoint

### PUB045 — Multi-root Extraction Baseline

- capture multiple roots in one run;
- aggregate deterministic root/class counts;
- validate each root independently;
- emit one coherent A3DM snapshot.

### PUB046 — Real Controlled Arma 3 Test Pack

- provide exact phone-readable instructions for PC execution;
- run a small real extraction;
- collect clipboard/RPT output;
- convert and validate it;
- record all engine-specific failures.

### PUB047 — Typed Property Coverage

- extend SQF extraction beyond four scalar fields;
- strings, numbers and arrays first;
- explicit diagnostics for unsupported config subclasses.

### PUB048 — SQF Batching and Checkpoints

- bounded chunks;
- persistent progress;
- interruption test;
- strict resume-context verification.

### PUB049 — First Partial Vanilla Snapshot

- selected roots;
- limited but useful property set;
- Browser loading and query tests;
- size, load-time and memory measurements.

### PUB050+ — Full Vanilla Candidate

- expand roots and properties;
- complete known relations;
- optimize storage and indexes;
- package a user-friendly local extractor/application;
- legal review before any prebuilt dataset distribution.

## 13. User test role

Until PUB045 is validated, no new manual test is required.

From PUB046, the user's role will be concrete:

1. launch Arma 3 with a specified minimal preset;
2. execute one supplied SQF command;
3. paste the resulting capture or attach the generated text;
4. provide the matching RPT marker and any SQF error;
5. repeat with a second preset only after the first is validated.

Tests will be small and sequential. The user will not be asked to extract every DLC or mod separately unless a specific diagnostic requires it.

## 14. Audit conclusions

The architecture is coherent. No redesign is required before multi-root work.

The main risk is no longer the query engine or Browser. The main risk is the real Arma-side acquisition layer: value typing, batching, engine limits, provenance and long-run reliability.

The correct next move is to stop expanding abstract components and push A3XE through controlled real extraction milestones.

Decision:

```text
PUB044 audit checkpoint
→ PUB045 multi-root
→ PUB046 first controlled real PC test
```
