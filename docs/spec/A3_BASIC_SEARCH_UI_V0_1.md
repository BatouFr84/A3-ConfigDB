# A3-ConfigDB Basic Search UI v0.1

PUB025 introduces the first Browser v2 user interface over the public artificial A3DM snapshot.

## Contract

The form submits the normalized A3QM payload to `POST /api/basic`:

```json
{
  "root": "CfgVehicles",
  "filters": [
    {"field": "scope", "operator": "eq", "value": 2}
  ],
  "limit": 100
}
```

The UI never calls A3QE or A3IX directly.

## Features

- Root selection from `/api/capabilities`.
- Dynamic add/remove filters.
- `eq` and property-item `contains` operators.
- Result limit from 1 to 500.
- Search, reset, loading, empty, success, and error states.
- Result table with display name, classname, root, and parent.
- Mobile-first single-column filter layout below 720 px.
- Artificial fixture badge and dataset metadata.

## Deliberate limits

- One local artificial snapshot only.
- No Advanced/A3QL editor yet.
- Result rows are prepared for selection but class sheets are not implemented.
- `contains` is exact membership in indexed structured properties, not text substring search.
- No export, sorting, pagination, or relation navigation.

## Data policy

PUB025 embeds no Arma 3 source dataset. The public service uses only `data/fixtures/a3dm_v0_1_example.json`, which declares `artificialDataOnly=true` and `sourceGameDataIncluded=false`.
