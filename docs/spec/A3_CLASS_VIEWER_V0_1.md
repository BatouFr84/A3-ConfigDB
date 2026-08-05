# A3 Class Viewer v0.1

PUB027 adds a browser-facing class viewer for artificial A3DM snapshots.

## Contract

- `GET /api/class/{root}/{classname}` returns one class.
- Response includes root, classname, parent, local properties and resolved properties.
- Unknown roots or classnames return `404 CLASS_NOT_FOUND`.
- Search result rows open the viewer.
- Basic mode displays selected resolved fields.
- Advanced mode renders local properties in an Arma-style C++ class block.

## Scope limits

This baseline does not yet provide full relation navigation, inverse references, deep nested C++ rendering, browser history or stable class URLs. Those remain later builds.

All public fixtures remain artificial and contain no real Arma 3 configuration data.
