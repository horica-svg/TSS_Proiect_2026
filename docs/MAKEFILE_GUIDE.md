# Makefile Guide

Acest ghid descrie comenzile active din Makefile, orientate pe rulare simpla pentru teste si structural coverage.

## Setup

1. Instaleaza dependintele:

```bash
make install
```

## Teste

1. Ruleaza toate testele:

```bash
make test
```

2. Ruleaza doar testele structurale:

```bash
make test-structural
```

## Structural Coverage (Target Unic)

Comanda principala:

```bash
make structural-cov KIND=<statement|branch|condition|paths> MODE=<statement|branch> HTML=<0|1>
```

Ce face fiecare argument:

- `KIND`
  - `statement`: foloseste fisierul `tests/structural_coverage/test_statement_coverage.py`
  - `branch`: foloseste fisierul `tests/structural_coverage/test_branch_coverage.py`
  - `condition`: foloseste fisierul `tests/structural_coverage/test_condition_coverage.py`
  - `paths`: foloseste fisierul `tests/structural_coverage/test_independent_paths_coverage.py`
- `MODE`
  - `statement`: line coverage
  - `branch`: branch coverage (`--cov-branch`)
- `HTML`
  - `0`: fara raport HTML
  - `1`: cu raport HTML in `htmlcov/`

Exemple:

```bash
# statement, fara html
make structural-cov KIND=statement MODE=statement HTML=0

# statement, cu html
make structural-cov KIND=statement MODE=statement HTML=1

# branch test, branch coverage, fara html
make structural-cov KIND=branch MODE=branch HTML=0

# condition test, line coverage, cu html
make structural-cov KIND=condition MODE=statement HTML=1
```

## Aliasuri rapide

```bash
make cov-statement
make cov-statement-html
```

Acestea sunt shortcut-uri pentru `KIND=statement` cu HTML `0` sau `1`.

## Auto-update expected pentru teste

Comenzi:

```bash
make expected-dry TARGET=statement
make expected-update TARGET=all
make expected-check TARGET=all
```

`TARGET` accepta: `all`, `statement`, `branch`, `condition`, `paths`.

Ce fac:

- `expected-dry`: arata diferentele detectate fara sa modifice fisiere.
- `expected-update`: recalculeaza si scrie valorile `expected` in testele structurale.
- `expected-check`: verifica drift-ul si intoarce cod de eroare daca exista diferente.

## Curatare artefacte

```bash
make clean
```

Sterge cache-ul de test, fisierele coverage si directorul `htmlcov/`.