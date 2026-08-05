# A3 Relations v0.1

PUB034 defines a stable, typed relation contract for class responses.

Supported relations:

- parent: same-root inheritance target;
- children: direct same-root subclasses;
- weapons: targets in CfgWeapons;
- magazines: targets in CfgMagazines;
- ammo: targets in CfgAmmo.

Each target is represented by `root`, `classname`, and `exists`. Missing roots or classes are never treated as valid. They are listed in `missingTargets`, and `complete` is false whenever at least one declared target cannot be resolved.

The resolver reads resolved properties for outbound relations so inherited arrays remain visible. Empty or absent properties produce empty relation lists, not errors.

PUB034 does not yet add clickable Browser navigation, reverse usage relations, deep turret traversal, or heuristic classname guessing.
