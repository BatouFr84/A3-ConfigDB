# A3XE Resolved Properties v0.1

PUB042 adds deterministic local and resolved property computation on top of the complete inheritance chains introduced by PUB041.

## Contract

For every extracted class, A3XE exposes:

- `local`: properties declared by the class itself;
- `resolved`: the effective property set after applying ancestors from root to leaf;
- `sources`: the classname that supplied each effective value.

Child values override parent values. Property names and classnames are serialized in deterministic order.

## Supported values

The resolver preserves JSON-compatible scalar, array and object values:

- null;
- string;
- boolean;
- integer and floating-point number;
- arrays of supported values;
- objects with string keys and supported values.

Any unsupported value is rejected explicitly. No stringification or silent omission is allowed.

## A3XE run output

The run envelope declares:

```json
{
  "selection": {"propertyMode": "local_and_resolved"},
  "resolvedProperties": {
    "root": "CfgWeapons",
    "complete": true,
    "classes": {}
  }
}
```

The A3DM snapshot remains backward compatible and continues to store the direct parent and local `properties`. Resolved values remain derived A3XE metadata in this baseline.

## Limits

PUB042 still uses the controlled SQF property allow-list from PUB039. Broader property discovery and native config value serialization remain future work.
