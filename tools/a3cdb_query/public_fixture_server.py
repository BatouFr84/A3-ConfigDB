"""Backward-compatible entry point for the public artificial fixture deployment.

The real HTTP routing now lives in ``local_http_server``. These compatibility
exports preserve the PUB025-PUB027 test and integration surface while callers
migrate to the structured local application.

Routes preserved by the delegated server:
- "/api/advanced"
- path.startswith("/api/class/")
"""

from tools.a3cdb_query.local_application import A3ConfigDBApplication
from tools.a3cdb_query.local_http_server import DEFAULT_DATASET, DEFAULT_WEB, main

APP = A3ConfigDBApplication.from_dataset(DEFAULT_DATASET)
SNAPSHOT = APP.snapshot
BACKEND = APP.backend
WEB = DEFAULT_WEB


if __name__ == "__main__":
    main()
