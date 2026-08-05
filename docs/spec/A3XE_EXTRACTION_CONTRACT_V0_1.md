# A3XE Extraction Contract v0.1

Status: PUB037 baseline.

## Purpose

A3XE extracts the configuration state of the exact Arma 3 session that the user launched. It does not reconstruct a theoretical vanilla baseline and it does not guess mod precedence. The loaded environment and its observed order are part of the extraction provenance.

The extraction output has two distinct layers:

1. an A3XE run envelope describing how the extraction happened;
2. the A3DM snapshot containing the extracted configuration state.

A completed run is publishable only when both layers validate and the snapshot digest matches.

## Environment provenance

The run envelope must record:

- Arma 3 product, version and build;
- platform and language when available;
- every loaded addon in observed load order;
- addon identifier, display name, version when available, and source category;
- active DLC identifiers;
- A3XE version and extraction run identifier.

`loadedAddons[].order` is authoritative provenance. It does not claim a universal DLC or mod order outside the extracted session.

## Extraction selection

The run records the requested roots and extraction modes. PUB037 defines:

- `propertyMode`: `local`, `resolved`, or `local_and_resolved`;
- `inheritanceMode`: `explicit_parent`;
- `relationMode`: `none` or `known_fields`.

The first real prototype should use `local_and_resolved`, `explicit_parent`, and `known_fields`.

## Class serialization

Each A3DM class must preserve:

- exact root;
- exact classname;
- explicit direct parent or `null`;
- local properties without inherited values mixed into them;
- resolved properties when requested;
- original scalar, array, object, boolean and null value types;
- deterministic key ordering at serialization time.

Unsupported values must never be silently converted to an empty string, zero, null or an empty array. They must produce a diagnostic and either a typed safe representation or an explicit skipped entry.

## Relations

Known relation fields may be derived from resolved properties after class serialization. PUB037 recognizes the relation families already consumed by the Browser:

- parent and children;
- vehicle weapons;
- weapon magazines;
- magazine ammo.

A missing target does not invalidate the source class. It must be retained as a missing relation target and must make the relation set incomplete.

## Progress and resume

A3XE must write progress independently from the final snapshot. The progress contract records totals, completed roots, discovered and serialized classes, and the last stable root/class cursor.

A resumed run must:

- use a new `runId`;
- set `resumeOf` to the previous run identifier;
- verify that the game build, loaded addon order, requested roots and extraction modes are unchanged;
- reject resume when any of those values differ;
- resume only after the last atomically committed class.

PUB037 defines the contract only. Resume implementation belongs to PUB040.

## Diagnostics

Diagnostics are split into `errors`, `warnings`, and `skipped`. Every entry has a stable code and message, plus optional root, classname and property context.

Rules:

- an error prevents `status=complete`;
- a skipped class or property must be named explicitly;
- warnings never hide missing data;
- aggregate counts must match the diagnostic arrays;
- no silent partial success is allowed.

## Completion and integrity

A run may declare `status=complete` only when:

- all selected roots are complete;
- serialized class count matches the committed snapshot content;
- diagnostics contain no errors;
- the A3DM validator passes;
- canonical JSON serialization succeeds;
- SHA-256 is calculated over the canonical snapshot payload;
- `integrity.complete` is true.

The final snapshot must be written to a temporary path and atomically renamed only after validation and digest generation. Interrupted temporary files are not valid datasets.

## Privacy and public boundary

A3XE extracts configuration data only. It must not include user names, profile paths, Steam identifiers, machine names, mission data, save data or arbitrary local file paths in the publishable snapshot.

Local diagnostic logs may contain a selected output path, but the A3DM package and public run manifest must not expose it.

## Formal schema

The machine-readable envelope is defined by:

`schemas/a3xe_extraction_contract_v0_1.schema.json`

The artificial reference instance is:

`data/fixtures/a3xe_extraction_contract_v0_1_example.json`

## Out of scope for PUB037

- SQF extraction code;
- extension or DLL transport;
- live progress UI;
- compression;
- resume execution;
- automatic upload;
- legal distribution of real extracted datasets.
