# A3DM v0.1 — Snapshot-First Dataset Model

Status: normative public draft after PUB016A.

A3DM v0.1 stores one complete, autonomous snapshot of the final Arma 3 master configuration observed during one extraction session. Arma 3 has already resolved addon load order, config patching and class inheritance before export.

## Core rule

One A3DM package equals one complete launch preset snapshot.

The package does not require a Vanilla baseline, per-addon extraction, profile dependency chain or differential reconstruction. The common user workflow is one extraction of the currently loaded game, DLC and mod preset.

## Provenance

The manifest records enough information to identify and reproduce the source environment where possible:

- Arma 3 version;
- extraction timestamp;
- active DLC identifiers when detectable;
- loaded addons/mods in observed load order;
- preset label supplied by the user;
- extractor version;
- artificial/source-data declarations.

Addon order is provenance metadata. A3DM does not replay addon precedence because the exported snapshot already contains the resolved final state.

## Snapshot payload

A snapshot contains complete logical classes grouped by config root. Each class stores its direct parent and properties as observed in the exported master config.

```json
{
  "snapshotId": "A3CDB_Test_Snapshot",
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
- a non-null parent must exist in the same root;
- inheritance cycles are invalid;
- properties preserve JSON scalar, array and object values;
- property absence and explicit JSON null are distinct;
- ordering has no semantic meaning except addon provenance order.

## Package structure

```text
a3dm-package/
├── manifest.json
├── snapshot.json or snapshot.json.zst
└── checksums.json
```

The combined artificial fixture used by public CI embeds `manifest` and `snapshot` in one JSON file. Production packaging may split them without changing their logical contract.

## Integrity

The production package will use deterministic SHA-256 checksums for every manifest-declared payload. Canonical serialization and compressed-container rules will be finalized before A3XE production export.

## Differential comparison

Differential profiles are not part of the core A3DM v0.1 storage model. Comparison between two autonomous snapshots belongs to the future A3DIFF component.

## Future Diagtor

Diagtor is the reserved name for the future dataset diagnostic tool. It is not part of the current implementation sequence.

## Compatibility

Readers fail closed on unsupported schema versions, malformed manifests, missing provenance fields, invalid roots, missing parents and inheritance cycles.
