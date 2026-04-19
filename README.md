# TSS_Proiect_2026

## Diagrame si modele

- CFG Mermaid pentru `TaxEngine.calculate_annual_tax`: `docs/tax_calculator_cfg_mermaid.md`
- Model profesoara (Java): `docs/model_profesoara/MyClassTest.java`

## Automation

Ghid complet Makefile:

- `docs/MAKEFILE_GUIDE.md`

### Teste

- `make test`
- `make test-structural`

### Structural Coverage

- `make structural-cov KIND=statement MODE=statement HTML=0`
- `make structural-cov KIND=statement MODE=statement HTML=1` (genereaza `htmlcov/index.html`)
- `make structural-cov KIND=branch MODE=branch HTML=0`
- `make cov-statement`
- `make cov-statement-html`

### Auto expected values

- `make expected-dry TARGET=statement`
- `make expected-update TARGET=all`
- `make expected-check TARGET=all`