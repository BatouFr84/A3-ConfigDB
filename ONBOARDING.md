# A3-ConfigDB Public Onboarding

This document is the entry point for users and contributors during the public-preview phase.

## What A3-ConfigDB is

A3-ConfigDB is an open-source platform for extracting, normalizing, indexing, querying and browsing Arma 3 configuration data generated locally by the user.

The public repository contains source code, documentation and artificial `A3CDB_Test_*` fixtures only. It does not distribute extracted Arma 3, DLC, cDLC or mod configuration databases.

## Current public preview

The current preview provides:

- a fixture-only Basic browser;
- a small artificial local dataset;
- a Python HTTP runtime;
- a Docker package;
- public CI covering the data boundary, licence, tests, Python compilation and Docker build.

The current preview does not yet provide the complete local extraction pipeline, production local-dataset import, full A3QL, inheritance and relation browsing, or unified exports.

## Quick start with Python

Requirements:

- Python 3.12 or later;
- no external Python package for the current fixture runtime.

From the repository root:

```bash
python tools/validate_public_staging.py
python -m unittest discover -s tests -p "test_*.py"
python tools/a3cdb_query/public_fixture_server.py
```

Open the local address printed by the server. The fixture browser should expose only artificial profiles and class names.

Health check:

```text
/healthz
```

Expected dataset status:

```json
{"status":"ok","dataset":"artificial"}
```

## Quick start with Docker

Build the image:

```bash
docker build -t a3-configdb-public-preview .
```

Run it:

```bash
docker run --rm -p 8000:8000 a3-configdb-public-preview
```

Then open:

```text
http://localhost:8000
```

The container must not require or download a real game-data database.

## Architecture baseline

The target platform is divided into explicit components:

- **A3 Core** — shared models, contracts and utilities;
- **A3DM** — Arma 3 Dataset Manager for local datasets and profiles;
- **A3IX** — local hybrid indexing engine;
- **A3QL** — Arma 3 Query Language;
- **A3QP** — strict versioned query parser;
- **A3QE** — query validation and execution engine;
- **A3RE** — inheritance, relation and sub-asset engine;
- **A3XE** — unified export engine;
- **A3 Runtime API** — local runtime boundary;
- **A3 Web API** — read-only browser-facing API;
- **A3 Browser** — Basic and Advanced user interface.

The intended default product is local-first. The user generates and keeps the real dataset on their own machine. Self-hosting remains possible, but the public project is not a hosted game-data service.

## Draft local dataset contract

The first production contract will be versioned and fail closed. A dataset package is expected to contain:

- a schema version;
- a dataset identifier;
- generation metadata;
- one or more profile identifiers;
- normalized configuration roots and assets;
- deterministic checksums;
- explicit declarations describing whether the package contains locally extracted game data;
- optional compressed payloads and generated indexes.

A profile represents a reproducible configuration environment. The planned storage model supports a baseline profile plus differential overlays so unchanged assets do not need to be duplicated across every profile.

The definitive schema does not exist yet. Contributors must not treat the current artificial fixture JSON as the final production format.

## Data and legal boundary

Never submit:

- extracted Arma 3, DLC, cDLC or mod databases;
- archives containing real configuration dumps;
- authentication secrets, private keys or service credentials;
- content obtained by bypassing ownership or access controls.

Synthetic fixtures must use the `A3CDB_Test_*` namespace and clearly declare that no source game data is included.

## Public-preview limitations

The current browser is a demonstration, not a complete release. In particular:

- searches operate only on artificial fixtures;
- performance on large local datasets is not represented;
- the local extractor is not implemented;
- the production importer and schema validator are not implemented;
- A3IX is not implemented;
- Advanced A3QL is not available in the public runtime;
- full asset sheets, inheritance, relations and sub-assets are not available;
- production exports are not available;
- mobile usability has not received a complete release pass.

## Contribution workflow

Before opening a pull request:

```bash
python tools/validate_public_staging.py
python -m unittest discover -s tests -p "test_*.py"
python -m py_compile tools/a3cdb_query/public_fixture_server.py
```

For runtime or packaging changes, also run:

```bash
docker build -t a3-configdb-public-preview .
```

Keep changes small, document the actual result and never weaken the public-data boundary to make a test pass.

## First public work items

The initial public issue set tracks:

1. the versioned local dataset contract;
2. the local extractor and importer boundary;
3. the A3IX hybrid index design;
4. Basic and Advanced browser requirements.

See `ROADMAP.md` for the full development sequence and `PUBLIC_STATUS.md` for the validated checkpoint.
