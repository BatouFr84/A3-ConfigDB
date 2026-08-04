# PUB012A — Public validator false-positive hotfix

## Status

`HOTFIX_APPLIED_VALIDATION_PENDING`

## Trigger

The first public `Validate Public Repository` run failed.

## Root cause

The public validator treated harmless mentions of denied identifiers as if they were exposed data. This included its own rule definitions and audit documentation. The rules were therefore self-rejecting.

## Correction

- Password and token checks now require a non-placeholder assigned value.
- Private dataset checks now require an actual path-like reference.
- Denied path components remain blocked without relaxation.
- Private-key detection remains unchanged.
- The complete AGPL, artificial fixture, required-file, symlink and file-size checks remain unchanged.

## Public hotfix head

`26b3a9d1471fdc175d07be90b2f737255c11e345`

## Validation

A new public workflow run is expected from this hotfix commit. No result is declared until GitHub Actions finishes.
