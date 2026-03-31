# TSS_Proiect_2026

## Diagrame si modele

- CFG Mermaid pentru `TaxEngine.calculate_annual_tax`: `docs/tax_calculator_cfg_mermaid.md`
- Model profesoara (Java): `docs/model_profesoara/MyClassTest.java`

## Automation

### Teste

- `make test`
- `make test-structural`
- `make test-file TEST=tests/structural_coverage/test_structural_coverage.py`

### Coverage (pytest-cov)

- `make cov`
- `make cov-branch`
- `make cov-html` (genereaza `htmlcov/index.html`)
- `make cov-xml`

### Mermaid build

- `make mermaid-build`