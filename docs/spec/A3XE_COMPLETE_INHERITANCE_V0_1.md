# A3XE Complete Inheritance v0.1

PUB041 reconstructs the complete root-to-class inheritance chain from the direct parent captured by SQF.

## Scope

- controlled `CfgWeapons` capture;
- direct parent remains the authoritative A3DM field;
- complete chains are derived deterministically by Python;
- missing parents and cycles are fatal;
- A3DM remains unchanged;
- the A3XE run receives an additive `inheritance` block containing `root`, `complete`, `chains`, and `maxDepth`.

## Command

```bash
python -m tools.a3xe_sqf_inheritance_converter capture.json build/a3xe-sqf
```

## Guarantees

Every serialized class has exactly one chain beginning at a captured root class and ending at itself. No inferred parent is invented. A capture truncated before a required parent is rejected rather than silently accepted.

## Current limit

The SQF prototype still works on one controlled root. Multi-root and external-parent closure are deferred.
