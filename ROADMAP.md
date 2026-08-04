# A3-ConfigDB Public Roadmap

This roadmap describes the intended direction of the public project. Checkpoints may be refined, but the data boundary is permanent: real game configuration databases are generated and controlled locally by the user and are not distributed by this repository.

## Phase 0 — Public foundation

- [x] Sanitized independent public repository
- [x] AGPL-3.0-or-later licensing
- [x] Artificial fixture dataset
- [x] Fixture-only Basic browser
- [x] Python and Docker runtime validation
- [x] Public continuous integration

## Phase 1 — Local dataset contract

- [ ] Versioned local dataset schema
- [ ] Import validation and diagnostics
- [ ] Compressed local dataset support
- [ ] Deterministic dataset manifest and checksums
- [ ] Explicit compatibility rules

## Phase 2 — Local extraction pipeline

- [ ] Arma 3-side export contract
- [ ] Local importer and normalizer
- [ ] Incremental profile generation
- [ ] P0 baseline plus differential profile overlays
- [ ] User documentation and recovery procedures

## Phase 3 — A3IX indexing

- [ ] Complete exact-value index
- [ ] Search-oriented text index
- [ ] Hybrid indexed and fallback execution
- [ ] Memory-bounded index generation
- [ ] Performance measurements on representative local datasets

## Phase 4 — Query platform

- [ ] Common normalized query model and AST
- [ ] Basic Query Builder generating visible A3QL
- [ ] Versioned A3QL grammar
- [ ] Strict A3QP parser
- [ ] A3QE validation and execution with precise errors
- [ ] Advanced A3QL editor, help and examples

## Phase 5 — Browser and relations

- [ ] Basic asset sheets
- [ ] Advanced C++-style configuration view
- [ ] Parent and inheritance navigation
- [ ] Incoming and outgoing relations
- [ ] Sub-assets and linked assets
- [ ] Mobile-first usability pass

## Phase 6 — Exports and distribution

- [ ] Unified A3XE export pipeline
- [ ] JSON, CSV and Markdown exports
- [ ] SQF Array and SQF HashMap exports
- [ ] Offline local server package
- [ ] Self-hosted Docker package
- [ ] Release documentation and upgrade path

## Target 1.0

A3-ConfigDB 1.0 should let a user generate configuration data from their own Arma 3 installation, load it locally, search it through Basic and Advanced A3QL modes, inspect inheritance and relations, and export results without uploading or redistributing the source dataset.

## Out of scope for the public repository

- hosting or distributing extracted Arma 3, DLC, cDLC or mod databases;
- bypassing ownership, licensing or access controls;
- new authentication development before the local and self-hosted products require it;
- irreversible dependence on a single cloud provider.
