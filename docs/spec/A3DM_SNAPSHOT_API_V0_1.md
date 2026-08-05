# A3DM Snapshot API v0.1

Status: implementation baseline.

The Snapshot API is the only supported read path for A3DM datasets. Browser, A3IX, A3QL/A3QE and future A3DIFF code must not read snapshot JSON structures directly.

## Responsibilities

- validate the complete snapshot before exposure;
- expose manifest provenance and snapshot identity;
- enumerate roots and classes deterministically;
- return immutable class data;
- resolve inherited properties using the class-parent chain already present in the exported Arma configuration;
- fail closed for unknown roots, classes or malformed packages.

## Python interface

```python
from tools.a3dm_snapshot import A3DMSnapshot

snapshot = A3DMSnapshot.from_file("dataset.json")
print(snapshot.game_version)
print(snapshot.roots)

for class_name, class_data in snapshot.iter_classes("CfgVehicles"):
    print(class_name, class_data["parent"])

properties = snapshot.resolved_properties(
    "CfgVehicles",
    "A3CDB_Test_Soldier",
)
```

## Immutability

Manifest, roots, classes, properties and nested arrays are recursively frozen after validation. Consumers cannot modify the loaded dataset accidentally. Derived indexes and browser state must be stored separately.

## Inheritance semantics

`get_class()` returns the exported class record and its directly defined properties. `resolved_properties()` walks the parent chain from the root parent to the requested class and applies later child definitions last.

This is class inheritance inside one final Arma snapshot. It is unrelated to the retired differential-profile model.

## Future compatibility

The API deliberately hides the physical storage representation. A later build may load split root files, compressed payloads or memory-mapped indexes without changing Browser or query-engine callers.
