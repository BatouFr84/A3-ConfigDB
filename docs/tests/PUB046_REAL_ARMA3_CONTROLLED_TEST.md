# PUB046 — First controlled real Arma 3 test

## What this test proves

This test verifies that Arma 3 can execute the current A3XE SQF exporter, place a real JSON capture in the clipboard, and produce data accepted by the existing Python conversion pipeline.

It does **not** yet test multi-root extraction, batching, resume or a complete Vanilla dataset.

## Files to copy

Copy the repository folder:

```text
a3xe/
```

into a temporary Arma 3 mission folder.

Required files:

```text
a3xe/sqf/fn_extractControlledRoot.sqf
a3xe/test/pub046/init.sqf
```

## Run in Arma 3

1. Open any empty test mission in Eden.
2. Start the mission locally.
3. Open the debug console.
4. Execute:

```sqf
[] execVM "a3xe\test\pub046\init.sqf";
```

5. Wait for the completion hint.
6. Paste the clipboard into a UTF-8 file named:

```text
capture.json
```

## Expected RPT markers

```text
A3XE_PUB046=START BUILD=PUB046
A3XE_SQF_EXPORT=PASS ROOT=CfgWeapons CLASSES=...
A3XE_PUB046=WAITING_FOR_CLIPBOARD
```

Any marker containing `A3XE_PUB046=FAIL` is a failure.

## Validate on the PC

From the repository root:

```bash
python -m tools.a3xe_pub046_capture_check capture.json
```

Expected:

```text
A3XE_PUB046_CAPTURE_CHECK=PASS
ROOT=CfgWeapons
CLASSES=...
GAMEVERSION=...
GAMEBUILD=...
```

Then convert it:

```bash
python -m tools.a3xe_sqf_capture_converter capture.json build/pub046-real
```

Expected files:

```text
build/pub046-real/snapshot.a3dm.json
build/pub046-real/a3xe-run.json
```

## PASS checklist

- Arma 3 displays the completion hint.
- The three expected RPT markers are present.
- The clipboard contains valid JSON.
- The capture checker returns `PASS`.
- The converter returns `A3XE_SQF_CONVERSION=PASS`.
- Both output files are created.
- No personal path, Steam ID or profile name appears in the capture.

## FAIL report to send

Send only:

```text
1. the exact RPT lines beginning with A3XE_
2. the checker output
3. the converter output
4. capture.json only if it contains no personal information
```

Do not send the full RPT unless specifically needed.

## Current controlled limits

```text
Root: CfgWeapons
Maximum classes: 100
Properties: displayName, scope, author, dlc
Output: clipboard + RPT markers
```
