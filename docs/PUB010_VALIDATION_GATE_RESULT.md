# PUB010 — Offline Staging Validation Gate Result

## Status

`REJECTED_REQUIRES_PUB010A`

## Staging repository

- Repository: `BatouFr84/A3-ConfigDB-Public-Staging`
- Branch: `main`
- Validation is manual-only while the repository remains private.

## Implemented in PUB010

- Added `tools/validate_public_staging.py`.
- Added fail-closed checks for forbidden paths, sensitive content, oversized files and symlinks.
- Added strict artificial fixture validation for `P0_TEST`, `P1_TEST` and `P2_TEST`.
- Added a complete-license gate requiring the official AGPL-3.0 markers and a minimum expected size.
- Updated `.github/workflows/staging-validation.yml` to execute the gate before tests and Docker build.

## Actual result

The current `LICENSE` is still the short staging notice and is not the complete, unmodified GNU AGPL version 3 text.

Therefore the gate must reject the current staging tree. No PASS is claimed and no GitHub Actions run was launched merely to confirm this deterministic failure.

## Required hotfix

`PUB010A` must:

1. Replace `LICENSE` with the complete, unmodified GNU Affero General Public License version 3 text.
2. Re-run the offline gate.
3. Run the manual staging workflow only after the offline gate is expected to pass.
4. Record the exact workflow conclusion and staging head.

## Publication state

The repository remains private. No rename, visibility change, merge or public activation is authorized.
