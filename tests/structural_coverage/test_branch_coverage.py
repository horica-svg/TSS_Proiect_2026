import pytest

from tests.structural_coverage.helpers import assert_tax_case


@pytest.mark.parametrize(
    "income, category, age, is_resident, has_dependents, is_married, expected",
    [
        # --- Validari initiale (Iesiri rapide) ---
        ("a", "salary", 20, True, False, False, "Error: Invalid Data Type"),
        (-1, "salary", 20, True, False, False, "Error: Invalid Income"),
        (3000, "salary", -1, True, False, False, "Error: Invalid Age"),
        (3000, "salari", 20, True, False, False, "Error: Invalid Category"),
        # --- Categoria Salary ---
        (3000, "salary", 24, True, False, True, 256.5),
        (20000, "salary", 65, True, False, True, 1900.0),
        (60000, "salary", 65, True, False, True, 7267.5),
        # --- Categoria Business ---
        (10000, "business", 65, True, False, True, 1520.0),
        (250000, "business", 65, True, False, True, 52487.5),
        (100000, "business", 65, True, False, True, 20187.5),
        # --- Categoria Investment ---
        (3000, "investment", 65, True, False, True, 290.7),
        (150000, "investment", 65, True, False, True, 19380.0),
        (50000, "investment", 40, False, False, True, 6412.5),
        # --- Categoria Freelance ---
        (60000, "freelance", 65, True, False, True, 6460.0),
        (1000, "freelance", 24, True, True, True, 0.0),
        (40000, "freelance", 40, False, True, True, 3289.5),
        # --- Categoria Crypto ---
        (15000, "crypto", 65, False, False, True, 2850.0),
        (5000, "crypto", 65, True, False, True, 380.0),
        # --- Categoria Real Estate ---
        (40000, "real_estate", 65, True, True, True, 1445.0),
        (75000, "real_estate", 40, False, True, True, 3825.0),
        (150000, "real_estate", 65, True, False, True, 14131.25),
        # --- Additional cases for branch coverage ---
        (60000, "salary", 45, True, False, False, 9000.0),
    ],
)
def test_branch_coverage(
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
