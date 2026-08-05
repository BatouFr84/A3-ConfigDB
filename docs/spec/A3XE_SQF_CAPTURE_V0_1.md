# A3XE SQF Capture v0.1

PUB039 introduces the first Arma 3-side extraction prototype.

## Scope

The prototype is deliberately restricted to:

- root `CfgWeapons`;
- direct classes visible under that root;
- explicit direct parent names;
- scalar properties `displayName`, `scope`, `author`, and `dlc`;
- a caller-supplied maximum class count.

It does not yet extract arrays, nested config classes, relations, complete addon metadata, or multiple roots.

## Arma 3 execution

From the debug console or a test mission:

```sqf
["CfgWeapons", 100] execVM "a3xe\sqf\fn_extractControlledRoot.sqf";
```

The script sorts classnames, creates one JSON capture, writes it to the clipboard, and emits an RPT marker:

```text
A3XE_SQF_EXPORT=PASS ROOT=CfgWeapons CLASSES=<n> BYTES=<n>
```

The clipboard payload must be saved locally as a UTF-8 JSON file. The public repository contains only an artificial fixture; no real Arma 3 config export is committed.

## Conversion

```bash
python -m tools.a3xe_sqf_capture_converter capture.json build/a3xe-sqf
```

Outputs:

```text
snapshot.a3dm.json
a3xe-run.json
```

The converter rejects:

- unsupported capture versions or sources;
- roots other than `CfgWeapons`;
- duplicate or empty classnames;
- unsupported properties;
- malformed parents;
- parents outside the controlled capture.

The generated snapshot is passed through `A3DMSnapshot`, so it uses exactly the same validation and loading path as the Browser.

## Privacy boundary

The SQF script must not read or serialize profile names, Steam identifiers, machine names, mission paths, save data, or arbitrary local paths.

## Limitations carried to PUB040+

- Clipboard transport is temporary.
- Real addon load-order discovery is not implemented.
- Captures are not resumable.
- Integrity is calculated after conversion, not inside Arma 3.
- Parent classes outside a truncated capture cause rejection.
- The prototype has not yet been validated against a user-produced real Arma 3 capture.
