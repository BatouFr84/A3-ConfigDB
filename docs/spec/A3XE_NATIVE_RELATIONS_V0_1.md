# A3XE Native Relations v0.1

PUB043 derives deterministic native relations from the direct-parent graph and the resolved properties produced by PUB042.

## Supported relations

- class to direct parent;
- parent to direct children;
- `weapons` to `CfgWeapons`;
- `magazines` to `CfgMagazines`;
- `ammo` to `CfgAmmo`.

## Source authority

Parent and children relations come from the explicit parent stored in A3DM. Outbound relations come from resolved properties. Each outbound target records `sourceClass`, which identifies the class that supplied the resolved property.

## Target validation

Each outbound target contains:

- `root`;
- `classname`;
- `exists`;
- `sourceClass`.

Missing targets are preserved in `missingTargets`; they are never silently discarded. Their presence sets `complete` to `false`.

## Determinism

Roots, classes, children, relation targets and missing-target diagnostics are sorted deterministically. Duplicate array targets are collapsed.

## A3XE run contract

The converter sets:

```json
{
  "selection": {"relationMode": "known_fields"},
  "nativeRelations": {
    "complete": true,
    "roots": {},
    "missingTargets": []
  }
}
```

The A3DM snapshot remains unchanged. Native relations are derived metadata in the A3XE run envelope for this baseline.

## Current limit

The controlled SQF capture still targets only `CfgWeapons` and does not yet extract relation fields. PUB043 therefore validates the complete relation engine with fixture data while preserving compatibility with the current real-SQF prototype.
