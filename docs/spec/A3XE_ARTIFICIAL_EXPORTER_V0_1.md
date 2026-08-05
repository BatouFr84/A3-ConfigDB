# A3XE Artificial Exporter v0.1

PUB038 implements the first executable A3XE pipeline without depending on Arma 3.

## Inputs

The exporter reads an artificial source document containing deterministic run metadata, environment metadata, manifest fields and root/class/property data.

## Outputs

The output directory receives:

- `snapshot.a3dm.json`: a normal A3DM package accepted by `A3DMSnapshot`, A3QE and the Browser backend.
- `a3xe-run.json`: the PUB037 extraction envelope with progress, diagnostics and SHA-256 integrity metadata.

## Guarantees

- deterministic ordering of roots and classes;
- explicit direct parents and local properties;
- inheritance validation before publication;
- validation through the same A3DM loader used by the application;
- canonical JSON SHA-256 digest;
- zero silent skipped values;
- atomic publication through temporary files and `os.replace`;
- no user, Steam, profile or machine-identifying data.

## Command

```bash
python -m tools.a3xe_artificial_exporter \
  data/fixtures/a3xe_artificial_source_v0_1.json \
  build/a3xe-artificial
```

The Browser loads the resulting `snapshot.a3dm.json` through the existing local dataset loader without a dedicated compatibility path.

## Deliberate limits

PUB038 does not read Arma 3 configuration data, does not run SQF, does not support interruption/resume and does not yet persist prebuilt A3IX indexes. Those concerns begin with PUB039 and PUB040.
