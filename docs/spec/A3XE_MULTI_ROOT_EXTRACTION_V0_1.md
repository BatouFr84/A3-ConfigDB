# A3XE Multi-root Extraction v0.1

## Scope

PUB045 allows one A3XE capture to contain several configuration roots and produce one autonomous A3DM snapshot.

Supported roots:

- `CfgWeapons`
- `CfgMagazines`
- `CfgAmmo`
- `CfgVehicles`

## Capture contract

The capture uses `captureVersion: "0.2"` and a `roots` object. Each root contains an array of classes with:

- `classname`
- direct `parent`
- local `properties`

Roots and classes are normalized deterministically. Duplicate classnames, unsupported roots, invalid properties and missing parents are rejected.

## Derived data

For every root, A3XE derives:

- complete inheritance chains;
- local and resolved properties;
- the source class of every resolved property.

Across all roots, A3XE derives known native relations:

- vehicle to weapons;
- weapon to magazines;
- magazine to ammo;
- parent to children.

Missing cross-root targets remain visible and set `nativeRelations.complete` to `false`. They are never hidden.

## Output

One conversion produces:

```text
snapshot.a3dm.json
a3xe-run.json
```

The snapshot contains all selected roots. The run envelope records global counters, root order, inheritance, resolved properties, relations and SHA-256 integrity.

## Determinism

- roots are sorted by root name;
- classes are sorted by classname;
- relation targets are sorted and deduplicated;
- the snapshot digest is calculated over canonical JSON.

## Explicit limits

This baseline validates the multi-root Python pipeline and an artificial representative capture. The Arma 3 SQF script still needs to emit the multi-root capture in a real session. Batching and persistent SQF checkpoints remain planned for later builds.
