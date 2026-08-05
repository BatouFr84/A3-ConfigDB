# A3 Local Dataset Loader v0.1

PUB030 introduces startup-time loading of one local A3DM snapshot selected through `A3CDB_DATASET`.

## Contract

- The application validates the selected file through `A3DMSnapshot.from_file`.
- A valid dataset enables capabilities, Basic queries, Advanced A3QL and class sheets.
- A missing or invalid dataset does not crash the HTTP process.
- Dataset-dependent routes return `503 DATASET_NOT_LOADED` until a valid snapshot is supplied.
- `GET /healthz` remains available and reports `datasetLoaded`.
- `GET /api/dataset` exposes the load state, selected path, validation error, snapshot identifier, roots, class count and manifest.

## Startup

```bash
A3CDB_DATASET=/path/to/snapshot.json python -m tools.a3cdb_query.local_http_server
```

The bundled artificial fixture remains the default for the public demonstration and Docker image.

## Out of scope

PUB030 does not add browser file upload, runtime hot reload, multiple simultaneous datasets, compressed packages or persistent user preferences.
