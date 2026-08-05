# A3-ConfigDB Local HTTP Application v0.1

PUB029 replaces the monolithic public fixture server with a structured local application baseline.

## Layers

1. `A3ConfigDBApplication` owns the loaded immutable snapshot and browser-facing operations.
2. `local_http_server.py` translates HTTP requests into application calls.
3. `web/` remains a static client and does not import query-engine internals.
4. `public_fixture_server.py` remains only as a backward-compatible entry point.

## Stable routes

- `GET /healthz`
- `GET /api/capabilities`
- `POST /api/basic`
- `POST /api/advanced`
- `GET /api/class/{root}/{classname}`

## Startup

```bash
python -m tools.a3cdb_query.local_http_server
```

Environment variables:

- `A3CDB_HOST` defaults to `127.0.0.1` for local safety;
- `PORT` defaults to `8080`;
- `A3CDB_DATASET` selects the snapshot file and currently defaults to the artificial fixture.

Docker explicitly sets `A3CDB_HOST=0.0.0.0` so the container remains externally reachable.

## Security and boundaries

- request bodies are limited to 65,536 bytes;
- static path traversal is rejected;
- malformed JSON and unknown routes return stable JSON errors;
- no upload route exists;
- no real Arma 3 data is distributed;
- PUB029 does not yet provide an interactive dataset loader.

## Compatibility

The Browser behavior from PUB027 is preserved. PUB030 may add controlled local dataset selection without changing the public API contract.
