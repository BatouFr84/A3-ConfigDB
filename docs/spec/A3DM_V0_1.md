# A3DM v0.1 — Local Dataset Model

Status: draft specification for public review.

A3DM defines the portable local data contract used by A3-ConfigDB. It separates a complete baseline profile from compact differential profiles while preserving deterministic reconstruction and exact query semantics.

## Permanent data boundary

The public repository contains schemas, software, documentation and artificial fixtures only. Real Arma 3, DLC, cDLC and mod configuration datasets are generated and retained locally by the user.

Every package must declare its schema version, package identity, baseline profile, profile dependencies, and whether it contains artificial or source-game data.

## Package structure

```text
a3dm-package/
├── manifest.json
├── profiles/
│   ├── P0_TEST.json
│   └── P1_TEST.delta.json
└── checksums.json
```

The manifest is authoritative. Profile files must not be discovered implicitly.

## Baseline profile

A baseline stores complete logical classes grouped by root:

```json
{
  "profileId": "P0_TEST",
  "kind": "baseline",
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
- `parent` is a class name in the same root or `null`;
- properties preserve JSON scalar, array and object values;
- property absence and explicit JSON `null` are distinct;
- ordering has no semantic meaning.

## Differential profiles

A delta profile stores ordered operations against one declared base profile.

Supported operations:

- `addClass`;
- `removeClass`;
- `setParent`;
- `setProperty`;
- `removeProperty`.

Example:

```json
{
  "profileId": "P1_TEST",
  "kind": "delta",
  "baseProfileId": "P0_TEST",
  "operations": [
    {
      "op": "setProperty",
      "root": "CfgVehicles",
      "className": "A3CDB_Test_Soldier",
      "property": "armor",
      "value": 25
    }
  ]
}
```

## Reconstruction

1. Load and validate the complete baseline.
2. Resolve the base-profile chain.
3. Reject cycles.
4. Apply operations in file order.
5. Reject any invalid operation instead of silently skipping it.
6. Expose a complete immutable logical profile to the query layer.

Preconditions:

- `addClass` requires the class to be absent;
- other class operations require the class to exist;
- `removeProperty` requires the property to exist;
- a non-null parent must resolve in the same root;
- removing a parent class is invalid until dependent classes are updated or removed.

## Removed versus null

A removed property uses `removeProperty`. A property intentionally set to JSON `null` uses `setProperty` with `value: null`.

- removed: the property no longer exists;
- null: the property exists and its value is null.

## Storage and query semantics

A class identical to its base is omitted from the delta. An empty delta is valid. Storage optimization must never affect query semantics: Basic and Advanced modes receive the same reconstructed class.

## Compatibility

A3DM v0.1 readers fail closed on unsupported schema versions, unknown operations and malformed required fields.

## Checksums

The package will use deterministic SHA-256 checksums for every manifest-declared payload. Canonical serialization details are reserved for the validator build.

## Owner decisions required

PUB015 asks the owner to validate these rules:

1. property deletion is explicit through `removeProperty`, never encoded as `null`;
2. class deletion is explicit through `removeClass`;
3. unchanged classes are absent from delta files;
4. each delta has one direct base profile, and chains are allowed;
5. invalid operations reject the complete profile;
6. the browser shows reconstructed state by default, with a future optional delta-inspection view.
