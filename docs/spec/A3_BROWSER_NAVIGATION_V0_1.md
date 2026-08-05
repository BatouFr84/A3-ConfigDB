# A3-ConfigDB Browser Navigation v0.1

## Status

PUB035 baseline.

## Scope

The class viewer can navigate through validated PUB034 relations without returning to search results.

Supported navigation targets:

- parent;
- children;
- weapons;
- magazines;
- ammo.

Missing relation targets remain visible but disabled. They are never opened as valid classes.

## History

The viewer keeps an in-session history with Back and Forward controls. Opening a result or a valid relation appends one entry. Navigating backward and then opening another relation truncates the forward branch.

## Stable URL

The active viewer state is represented by query parameters:

```text
?root=CfgVehicles&class=A3CDB_Test_Soldier&view=basic
```

The `view` value is `basic` or `advanced`. Loading such a URL opens the requested class after capabilities are available.

## Browser integration

The browser History API is used through `pushState`, `replaceState`, and `popstate`. Search mode and viewer mode remain separate.

## Limits

This baseline does not provide breadcrumbs, deep graph traversal, inverse relations beyond children, cross-dataset links, or server-side permanent routes.
