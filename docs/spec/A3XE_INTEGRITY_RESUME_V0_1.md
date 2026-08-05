# A3XE Integrity and Resume v0.1

## Status

PUB040 baseline.

## Purpose

Long Arma 3 configuration extractions must survive interruption without mixing data from different game or mod environments. A resume state is therefore valid only for the exact extraction context that created it.

## Resume-critical context

The context fingerprint is a canonical SHA-256 digest of:

- `gameVersion`
- `gameBuild`
- `loadedAddons`, including observed order
- `activeDlc`
- selected `roots`
- `propertyMode`
- `inheritanceMode`
- `relationMode`

Any difference rejects resume explicitly. Addon order is significant.

## State lifecycle

```text
running
  -> checkpoint(s)
  -> integrity verification
  -> complete
```

A complete state has:

```json
{
  "status": "complete",
  "resumePossible": false,
  "integrityState": "verified"
}
```

A completed extraction cannot be resumed.

## Checkpoints

Each checkpoint records:

- completed roots;
- discovered classes;
- serialized classes;
- last root;
- last classname.

Counters are monotonic. Serialized classes cannot exceed discovered classes. Completed roots cannot exceed selected roots.

The state file is written through a temporary file followed by `os.replace`, preventing a partially written checkpoint from replacing the last valid state.

## Final integrity gate

Completion requires:

1. all roots complete;
2. all discovered classes serialized;
3. valid A3DM package;
4. exact class-count agreement;
5. valid direct parents;
6. resolvable inheritance chains;
7. canonical JSON serialization;
8. SHA-256 snapshot digest.

Failure at any gate leaves the run incomplete and raises an explicit error.

## Public boundary

The resume state stores extraction context only. It must not include Steam identifiers, profile names, computer names, arbitrary local paths, saves or mission content.

## Current limitation

PUB040 provides the reusable state and integrity primitives. Automatic checkpoint emission from the live SQF loop and multi-session continuation are wired progressively in later A3XE builds.
