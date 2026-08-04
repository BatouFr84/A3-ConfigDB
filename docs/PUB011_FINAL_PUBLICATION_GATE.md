# PUB011 — Final Publication Gate

Date: 2026-08-04

## Scope

This gate evaluates the sanitized public staging repository only. It does not authorize changes to the private A3-ConfigDB repository, PR #16, or any private dataset.

## Validated evidence

- Static data-boundary audit: PASS.
- Forbidden private markers and secrets: absent in the staging snapshot.
- Artificial fixtures only: PASS.
- Complete GNU AGPL v3 license text: PASS.
- Python unit tests: PASS (2 tests discovered and executed).
- Python compilation: PASS.
- Runtime `/healthz`: PASS.
- Runtime Basic artificial query: PASS.
- Real Docker image build on Render: PASS.
- Container start on Render: PASS.
- Mobile page load: PASS.
- Mobile artificial Basic query: PASS.
- Real Arma 3 data exposure: none observed.

Validated Render URL at the time of the gate:

`https://a3-configdb-public-staging-docker.onrender.com`

## Repository state

- Repository: `BatouFr84/A3-ConfigDB-Public-Staging`.
- Default branch: `main`.
- Visibility: private.
- History: independent from the private A3-ConfigDB repository.
- Render-only branch: `validation/render-docker`; it must not be merged into `main`.

## Verdict

`PUBLICATION_GATE=PASS_WITH_OWNER_TRANSITION_REQUIRED`

The sanitized `main` branch is technically suitable to become the public A3-ConfigDB repository. The transition is not performed automatically because repository rename and visibility changes are irreversible owner-level actions and because the existing private repository must first retain a distinct private name.

## Required owner transition order

1. Keep `BatouFr84/A3-ConfigDB` private and rename it to `A3-ConfigDB-Private`.
2. Keep PR #16 open and draft; do not merge or close it.
3. Rename `BatouFr84/A3-ConfigDB-Public-Staging` to `A3-ConfigDB`.
4. Confirm `main` remains the default branch.
5. Change only the renamed staging repository visibility to public.
6. Do not merge `validation/render-docker` into `main`.
7. After the repository is public, run one public validation workflow and verify it is green.
8. Remove the temporary Render service when no longer needed.

## Functional boundary

The current public snapshot is a minimal artificial-fixture demonstration. It is not yet the full local extractor, A3IX index engine, Advanced A3QL browser, relation explorer or production local database application. Those capabilities belong to subsequent public development stages.
