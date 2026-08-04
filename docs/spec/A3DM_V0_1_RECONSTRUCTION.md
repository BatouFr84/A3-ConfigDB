# A3DM v0.1 — Reconstruction examples

All examples use artificial `A3CDB_Test_*` fixtures.

## Baseline state

`P0_TEST` contains:

```text
A3CDB_Test_Soldier
armor = 20
obsoleteProperty = "remove me"
```

`A3CDB_Test_Scout` does not exist.

## Delta operations

`P1_TEST` applies:

1. `setProperty armor = 25` on `A3CDB_Test_Soldier`;
2. `removeProperty obsoleteProperty`;
3. `addClass A3CDB_Test_Scout` inheriting from `A3CDB_Test_Soldier`.

## Reconstructed state

The logical `P1_TEST` result is:

```cpp
class A3CDB_Test_Soldier: A3CDB_Test_Man
{
    displayName = "A3CDB Test Rifleman";
    armor = 25;
    scope = 2;
    linkedItems[] = {"A3CDB_Test_Helmet", "A3CDB_Test_Vest"};
};

class A3CDB_Test_Scout: A3CDB_Test_Soldier
{
    displayName = "A3CDB Test Scout";
    armor = 15;
    scope = 2;
};
```

`obsoleteProperty` is absent, not null.

## Expected query behaviour

- searching `armor = 20` in `P0_TEST` returns `A3CDB_Test_Soldier`;
- searching `armor = 25` in `P1_TEST` returns `A3CDB_Test_Soldier`;
- searching for `obsoleteProperty` in `P1_TEST` returns no property on that class;
- searching `className = A3CDB_Test_Scout` in `P1_TEST` returns the added class;
- Basic and Advanced modes receive the same reconstructed logical state.

## Failure examples

The profile must be rejected when a delta:

- removes a missing property;
- adds a class that already exists;
- references a missing base profile;
- creates a dependency cycle;
- sets a parent that does not resolve;
- uses an unknown operation.
