# A3DM v0.1 — Snapshot consumption

Status: supersedes the earlier baseline-plus-delta reconstruction draft.

A3DM v0.1 packages are autonomous snapshots. No profile chain is reconstructed during normal use.

## Load sequence

1. Read and validate the manifest.
2. Verify package identity and integrity metadata.
3. Validate the snapshot structure.
4. Validate parent references and inheritance cycles inside each config root.
5. Expose the complete immutable snapshot to A3IX, A3QL, Basic and Advanced browser modes.

## Arma 3 responsibility

Arma 3 resolves addon load order, config patching and class inheritance before A3XE exports the master configuration. The recorded addon list and order describe provenance; A3-ConfigDB does not replay those addons.

## Example

The artificial fixture contains a complete `CfgVehicles` state:

```cpp
class A3CDB_Test_Man
{
    displayName = "A3CDB Test Man";
    armor = 10;
    scope = 1;
};

class A3CDB_Test_Soldier: A3CDB_Test_Man
{
    displayName = "A3CDB Test Rifleman";
    armor = 20;
    scope = 2;
    linkedItems[] = {"A3CDB_Test_Helmet", "A3CDB_Test_Vest"};
};
```

Basic and Advanced modes consume this same final snapshot.

## Comparison

Differences between two snapshots are calculated later by A3DIFF. They are not required for loading or querying either dataset.
