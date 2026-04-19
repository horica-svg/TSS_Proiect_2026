import pytest

from tests.structural_coverage.helpers import assert_tax_case


@pytest.mark.parametrize(
    "income, category, age, is_resident, has_dependents, is_married, expected",
    [
        # --- Validari initiale (P1, P3, P5, P7) ---
        ("a", "salary", 20, True, False, False, "Error: Invalid Data Type"),
        (-1, "salary", 20, True, False, False, "Error: Invalid Income"),
        (3000, "salary", -1, True, False, False, "Error: Invalid Age"),
        (3000, "salari", 20, True, False, False, "Error: Invalid Category"),
        # --- Categorii + ajustari (P9-P24, P26) ---
        (4000, "salary", 20, True, False, False, 360.0),
        (300000, "business", 30, True, False, False, 80000.0),
        (4000, "investment", 30, True, False, False, 510.0),
        (60000, "freelance", 30, True, True, True, 6375.0),
        (50000, "crypto", 30, False, False, False, 19500.0),
        (70000, "real_estate", 40, True, False, True, 4275.0),
        # --- Ramuri seniori (P17 si P19) ---
        (20000, "salary", 70, True, False, False, 2000.0),
        (40000, "salary", 70, True, False, False, 4675.0),
    ],
)
def test_independent_paths_circuits(
    engine,
    income,
    category,
    age,
    is_resident,
    has_dependents,
    is_married,
    expected,
):
    assert_tax_case(
        engine,
        income,
        category,
        age,
        is_resident,
        has_dependents,
        is_married,
        expected=expected,
    )


def test_independent_paths_circuit_p25_forced(engine, monkeypatch):
    # P25 este infezabil in flux normal; forțam max(0, tax) sa lase valoarea negativa.
    monkeypatch.setattr("builtins.max", lambda _min_value, current_tax: current_tax)

    result = engine.calculate_annual_tax(
        income=1000,
        category="freelance",
        age=30,
        is_resident=True,
        has_dependents=True,
        is_married=False,
    )

    # Ramura finala P25 (tax < 0) normalizeaza rezultatul la 0.
    assert result == 0
