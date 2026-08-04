# PUB010A — Quota-constrained AGPL completion

Status: `BLOCKED_PENDING_LICENSE_INSTALL_AND_OFFLINE_VALIDATION`

GitHub Actions minutes are exhausted for the current billing period. No workflow was launched.

Implemented:

- dependency-free installer for the canonical GNU AGPL v3 text;
- minimum-size and required-section checks;
- HTML/truncation rejection;
- atomic replacement of `LICENSE`;
- SHA-256 reporting;
- existing publication validator remains blocking.

Required before public release:

1. Run `python tools/install_official_agpl.py` in a real checkout with network access.
2. Run `python tools/validate_public_staging.py`.
3. Run the unit tests and Python compilation locally.
4. After GitHub Actions minutes reset, run the single manual staging-validation workflow once.

Until all four checks pass, the repository must remain private and must not be renamed or promoted as the public release.
