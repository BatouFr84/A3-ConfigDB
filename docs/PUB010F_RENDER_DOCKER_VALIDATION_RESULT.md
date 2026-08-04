# PUB010F — Render Docker Validation Result

## Scope

Validate the public staging Docker image without consuming private GitHub Actions minutes.

## Provider result

- Provider: Render
- Service: `a3-configdb-public-staging-docker`
- Source branch: `validation/render-docker`
- Reported deployment state: `Live`
- Public URL: `https://a3-configdb-public-staging-docker.onrender.com`

## Validation status

- Docker image build: **PASS** — Render reached `Live`, which requires a successful Docker build and container start.
- Container start: **PASS** — service reported `Live`.
- HTTP smoke test from the assistant environment: **NOT RUN** — the execution environment could not resolve the Render hostname.
- User-side HTTP smoke test: **PENDING**.

## Required user-side checks

1. Open `/healthz` and confirm an HTTP 200 JSON response containing `status: ok` and `dataset: artificial`.
2. Open `/` and confirm the artificial fixture demo loads.
3. Submit a Basic search using profile `P0_TEST`, root `CfgVehicles`, field `displayName`, value `Rifleman`.
4. Confirm the result contains only `A3CDB_Test_*` data.

## Boundaries

- No GitHub Actions workflow was triggered.
- `main` remains unchanged.
- `validation/render-docker` remains temporary and must never be merged.
- Public release authorization remains pending until the HTTP smoke test passes.
