# A3DM v0.1 — Local Dataset Model

Status: owner-approved semantic baseline.

A3DM is the portable local data contract used by A3-ConfigDB. It follows the useful parts of Arma 3 configuration inheritance: a complete baseline is loaded first, later profiles are applied in an explicit linear order, inherited values remain available, and the last valid definition wins.

## Permanent data boundary

The public repository contains schemas, software, documentation and artificial fixtures only. Real Arma 3, DLC, cDLC and mod configuration datasets are generated and retained locally by the user.

## Package model

A package contains one complete baseline profile and zero or more differential profiles declared by an authoritative manifest. The manifest is authoritative; profile files are never discovered implicitly.

## Baseline profile

The baseline stores complete logical classes grouped by root. Class names and property names are case-sensitive. A parent is either `null` or a class in the same root. Property absence and explicit JSON `null` are distinct.

## Differential profiles

Each delta declares exactly one direct base profile. Chains are linear, for example `P0 → P1 → P2`.

Supported operations:

- `addClass` — add a class that does not exist;
- `removeClass` — remove a class only when no remaining class inherits from it;
- `setParent` — replace a class parent with an existing class in the same root or `null`;
- `setProperty` — define or redefine one property.

There is no generic `removeProperty` operation in v0.1. An inherited property remains inherited unless a later profile redefines it.

## Arma-style precedence

Profiles are reconstructed from the baseline toward the requested profile. Operations are applied in array order. When several valid operations define the same property, the last applied definition wins.

```text
P0 armor = 20
P1 armor = 25
P2 armor = 30
Final P2 armor = 30
```

A class unchanged from its base is not repeated in the delta.

## Fail-closed reconstruction

The complete requested profile is rejected when any operation is incoherent. Nothing is silently ignored and no partially reconstructed profile is exposed.

Rejected cases include:

- modifying or removing a missing class;
- adding an existing class;
- assigning a missing parent;
- creating an inheritance cycle;
- removing a class still used as a parent;
- unknown operations;
- unsupported schema versions;
- profile dependency cycles or missing base profiles.

Errors identify the profile and operation index.

## Browser semantics

Basic and Advanced modes consume the same immutable reconstructed state. The default class sheet shows the complete final class. A future secondary view may show raw delta operations and provenance.

## Arrays and nested structures

`setProperty` replaces the complete JSON value in v0.1, including arrays and objects. Arma-style additive array syntax such as `+=` is deferred until its ordering and inheritance semantics can be represented without ambiguity.

## Compatibility and checksums

Readers fail closed on unsupported schema versions. Deterministic SHA-256 checksums are required for production packages; canonical serialization and package-directory validation will be finalized later.

## Owner-approved rules

1. no generic property deletion in v0.1;
2. class deletion is explicit and dependency-safe;
3. unchanged classes are absent from deltas;
4. one direct base per delta, with linear chains;
5. the last valid definition wins;
6. any inconsistency rejects the complete profile;
7. reconstructed state is the primary browser view.
