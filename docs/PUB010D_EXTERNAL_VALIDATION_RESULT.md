# PUB010D — External Validation Result

Status: `PARTIAL_EXTERNAL_PASS_DOCKER_PENDING`

## Scope executed outside GitHub Actions

- `python -m unittest discover -s tests -p 'test_*.py'`
- `python -m py_compile tools/a3cdb_query/public_fixture_server.py`
- HTTP smoke test against `/healthz`
- HTTP Basic fixture query against `/api/basic`

## Result

- Unit tests: PASS (`2 tests`)
- Python compilation: PASS
- HTTP health check: PASS
- HTTP Basic fixture query: PASS
- Docker build: NOT RUN (`docker` unavailable in the external execution environment)
- GitHub Actions consumed: 0

## Defects corrected during PUB010D

- The staging validator referenced nonexistent paths (`NOTICE.md`, `public_fixture_dataset_v1.json`, `test_public_boundary.py`).
- The test suite used pytest-style free functions while the workflow invoked `unittest discover`, which resulted in zero discovered tests.
- The validator and test suite now match the actual sanitized snapshot (`NOTICE`, `public_fixture.json`, `test_public_fixture.py`, profiles `P0_TEST` and `P1_TEST`).

## Gate

The Python runtime and fixture-only Basic API are externally validated. Public release remains blocked until one Docker build succeeds in a suitable environment. The repository remains private and no workflow has been launched.
