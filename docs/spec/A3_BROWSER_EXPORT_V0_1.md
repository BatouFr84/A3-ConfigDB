# A3-ConfigDB Browser Export v0.1

PUB036 adds client-side deterministic exports for complete result sets and the currently opened class.

## Result exports

Supported formats: JSON, CSV, Markdown and SQF Array.

A result export is refused when the current response declares a `total` different from the number of loaded result items. This prevents a paginated or truncated page from being silently presented as a complete export.

## Class exports

Supported formats: JSON, Markdown, SQF Array and C++ config view. Class exports use the complete class response already loaded by the Browser, including local properties, resolved properties and relations.

## Filenames

Files use deterministic sanitized names beginning with `a3configdb_`. Result filenames include the snapshot identifier. Class filenames include the root and classname.

## Scope limits

PUB036 does not add server-side streaming, ZIP packages, export templates, selected columns, multi-page aggregation or bulk relation traversal.
