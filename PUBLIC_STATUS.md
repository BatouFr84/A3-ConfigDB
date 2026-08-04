# Public Project Status

## Current checkpoint

`PUB013 — Public repository cleanup and roadmap baseline`

## Validated foundation

The public repository has passed the following gates:

- sanitized repository boundary validation;
- artificial fixtures only;
- complete GNU AGPL v3 license validation;
- Python unit tests;
- Python runtime compilation;
- native runtime smoke tests;
- real Docker image build on Render;
- mobile HTTP health, interface and Basic-query smoke tests;
- public GitHub Actions validation after the PUB012A false-positive hotfix.

## Current capabilities

- fixture-only Basic search;
- synthetic P0_TEST and P1_TEST profiles;
- read-only HTTP runtime;
- responsive demonstration interface;
- Docker deployment;
- public CI validation.

## Explicit limitations

The public preview does not yet include:

- extraction from a local Arma 3 installation;
- loading a user-generated local database;
- complete hybrid indexing;
- Advanced A3QL execution;
- full asset sheets, relations and sub-assets;
- unified exports;
- offline desktop packaging.

No real Arma 3, DLC, cDLC or mod configuration data is distributed.

## Repository boundary

The historical development repository remains private under `A3-ConfigDB-private`. This public repository has an independent sanitized history.

The temporary branch `validation/render-docker` was used solely for external Docker validation. It must not be merged into `main` and may be deleted manually after the associated Render service is no longer needed.
