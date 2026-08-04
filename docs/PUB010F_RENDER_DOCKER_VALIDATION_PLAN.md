# PUB010F — Render Docker validation plan

Status: PREPARED_REQUIRES_PROVIDER_EXECUTION

This temporary branch exists only to validate the public staging Docker image without using GitHub Actions minutes.

## Branch

`validation/render-docker`

## Render configuration

- Runtime: Docker
- Dockerfile: `./Dockerfile`
- Build context: repository root
- Region: Frankfurt
- Plan: Free
- Health check: `/healthz`
- Auto-deploy: disabled

## Required provider-side validation

1. Create a new Render Blueprint or Web Service from `BatouFr84/A3-ConfigDB-Public-Staging`.
2. Select branch `validation/render-docker`.
3. Confirm Docker runtime and `./Dockerfile`.
4. Deploy once manually.
5. Confirm the build completes successfully.
6. Confirm `/healthz` returns HTTP 200 with an artificial dataset status.
7. Submit a Basic query against `/api/basic` and confirm HTTP 200 with only `A3CDB_Test_*` records.
8. Record the deploy identifier, service URL and result.
9. Delete the temporary Render service after validation.

## Safety boundaries

- The staging repository remains private.
- No real Arma 3 dataset is present.
- No authentication secret is required.
- Auto-deploy remains disabled.
- `main` is unchanged.
- `render.yaml` exists only on the temporary validation branch and must never be merged into the public main branch.

Publication remains denied until the Docker build and container smoke tests are confirmed.