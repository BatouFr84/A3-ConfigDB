# A3IX Property Index v0.1

Status: PUB019 baseline.

This component builds an immutable contains-index from resolved A3DM snapshot properties. It targets frequent technical searches that would otherwise require a complete class scan.

## Default indexed properties

- `linkedItems`
- `weapons`
- `magazines`
- `turrets`
- `transportItems`

## Semantics

Text matching is exact and case-insensitive. Numeric and boolean values remain typed. Arrays and nested objects are traversed recursively and scalar leaves are indexed. Duplicate occurrences inside one asset produce only one asset reference.

The index consumes resolved properties, so inherited values remain searchable. Results are deterministic tuples ordered by root and classname. An unknown property path fails explicitly; PUB019 does not silently fall back to a slow scan.

## Example

```python
index.contains("linkedItems", "NVGoggles_B")
index.contains("magazines", "30Rnd_65x39_caseless_mag", root="CfgVehicles")
```

## Scope limits

This baseline does not yet provide substring matching, arbitrary dotted-path selection, persistence, compression, query planning or hybrid fallback. Those belong to later A3IX and A3QE builds.
