# A3-ConfigDB

A3-ConfigDB is an open-source configuration exploration platform for Arma 3 datasets generated locally by the user from content they are legitimately entitled to access.

The public repository contains software, documentation, schemas and artificial `A3CDB_Test_*` fixtures only. It does not distribute Arma 3, DLC, cDLC or mod configuration databases.

## Public preview status

A3-ConfigDB is now public as an early functional preview. The current repository provides:

- a fixture-only Basic browser;
- an artificial dataset boundary suitable for demonstrations and tests;
- a validated Python runtime;
- a validated Docker image;
- public continuous integration for boundary, license, tests, compilation and Docker build checks.

The current preview is not yet the complete local Arma 3 extraction and browsing tool. Advanced A3QL, local dataset generation, full relations, sub-assets and unified exports remain planned work.

See [`PUBLIC_STATUS.md`](PUBLIC_STATUS.md) for the current checkpoint and [`ROADMAP.md`](ROADMAP.md) for the planned development sequence.

## Official usage modes

- **Public Demo** — artificial fixtures only.
- **Local Database** — the recommended future mode; users generate and index their own data locally.
- **Self-hosted Server** — users may host the application with their own locally generated database, subject to applicable rights and the project license.

A3-ConfigDB is not a hosted game-data service. Real configuration data remains under the control of the user who generated it.

## Data policy

No real Arma 3 configuration database is included in this repository. Public fixtures use only synthetic `A3CDB_Test_*` class names and values. See [`DATA_POLICY.md`](DATA_POLICY.md).

## Development disclosure

The project is developed with extensive AI assistance under human direction, review and functional validation. See [`AI_DISCLOSURE.md`](AI_DISCLOSURE.md).

## License

A3-ConfigDB is licensed under the GNU Affero General Public License, version 3 or later (`AGPL-3.0-or-later`). See [`LICENSE`](LICENSE).

## Independence notice

Arma 3 and related names are trademarks of their respective owners. A3-ConfigDB is an independent community project and is not affiliated with, sponsored by or endorsed by Bohemia Interactive.
