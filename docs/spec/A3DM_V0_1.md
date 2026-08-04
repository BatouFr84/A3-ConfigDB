# A3DM v0.1 — Local Snapshot Dataset Model

Status: owner-approved snapshot-first semantic baseline.

A3DM is the portable local data contract used by A3-ConfigDB. One package represents one complete autonomous snapshot of the final Arma 3 master configuration observed during one extraction session.

## Permanent data boundary

The public repository contains schemas, software, documentation and artificial fixtures only. Real Arma 3, DLC, cDLC and mod configuration datasets are generated and retained locally by the user.

## Snapshot-first rule

The common workflow is one extraction of the user's currently loaded game, DLC and mod preset. A3DM does not require:

- a separate Vanilla extraction;
- one extraction per DLC or mod;
- a baseline-plus-delta dependency chain;
- replaying addon priority during import.

Arma 3 has already resolved addon load order, config patching and class inheritance before export. A3DM stores that final state.

## Provenance manifest

The manifest records:

- A3DM schema and package version;
- dataset and snapshot identifiers;
- extraction timestamp;
- extractor version;
- Arma 3 version;
- user-facing preset label;
- active DLC identifiers when detectable;
- loaded addons/mods in observed load order;
- artificial/source-data declarations.

Addon order is provenance metadata used to identify and reproduce the source environment. It is not a reconstruction instruction.

## Snapshot payload

The snapshot contains complete logical classes grouped by config root.

```json
{
  "snapshotId": "A3CDB_Test_Snapshot_01",
  "roots": {
    "CfgVehicles": {
      "A3CDB_Test_Soldier": {
        "parent": "A3CDB_Test_Man",
        "properties": {
          "displayName": "A3CDB Test Rifleman",
          "armor": 20,
          "scope": 2
        }
      }
    }
  }
}
```

Rules:

- roots and class names are case-sensitive;
- class names are unique within a root;
- a parent is either `null` or a class in the same root;
- inheritance cycles are invalid;
- properties preserve JSON scalar, array and object values;
- property absence and explicit JSON `null` are distinct;
- ordering has no semantic meaning except the recorded addon load order.

## Validation

Readers fail closed on:

- unsupported schema versions;
- missing required provenance fields;
- snapshot identity mismatches;
- invalid or duplicate addon-order entries;
- malformed roots or classes;
- missing parents;
- inheritance cycles;
- contradictory artificial/source-data declarations.

## Storage and compression

The logical package contains `manifest`, `snapshot` and checksums. Production packaging may store the snapshot as JSON or compressed JSON/Zstandard without changing its logical contents.

Deterministic SHA-256 checksums and canonical serialization are required before production A3XE export is declared stable.

## Comparison

Differential storage is not part of core A3DM v0.1. Comparing two autonomous snapshots belongs to the future A3DIFF component.

## Future Diagtor

Diagtor is the reserved name for the future dataset diagnostic tool. It remains outside the current implementation sequence.
