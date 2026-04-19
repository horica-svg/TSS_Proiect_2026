import pytest
from tests.structural_coverage.helpers import assert_tax_case


@pytest.mark.parametrize(
    "income, category, age, is_resident, has_dependents, is_married, expected",
    [
        # --- Validări inițiale ---
        ("a", "salary", 20, True, False, False, "Error: Invalid Data Type"),
        (-1, "salary", 20, True, False, False, "Error: Invalid Income"),
        (3000, "salary", -1, True, False, False, "Error: Invalid Age"),
        (3000, "salari", 20, True, False, False, "Error: Invalid Category"),
        # --- Decizii simple (Branch Coverage) ---
        (100000, "business", 40, True, False, False, 25000.0),
        (250000, "business", 40, True, False, False, 65000.0),
        (3000, "investment", 40, True, False, False, 382.5),
        (50000, "investment", 40, True, False, False, 7500.0),
        (150000, "investment", 40, True, False, False, 24000.0),
        (40000, "real_estate", 40, True, False, False, 2000.0),
        (75000, "real_estate", 40, True, False, False, 5000.0),
        (150000, "real_estate", 40, True, False, False, 17500.0),
        (5000, "crypto", 40, True, False, False, 500.0),
        (1000, "freelance", 40, True, True, False, 0.0),
        # --- MC/DC: income >= 50000 (C1) and is_resident (C2) ---
        (
            60000,
            "freelance",
            40,
            True,
            False,
            False,
            8000.0,
        ),  # C1=T, C2=T -> Rezultat: T
        (
            40000,
            "freelance",
            40,
            True,
            False,
            False,
            4800.0,
        ),  # C1=F, C2=T -> Rezultat: F
        (
            60000,
            "freelance",
            40,
            False,
            False,
            False,
            6480.0,
        ),  # C1=T, C2=F -> Rezultat: F
        # --- MC/DC: (age < 25 (C1) and income < 5000 (C2)) or (not is_resident (C3) and category != 'crypto' (C4)) ---
        (
            4000,
            "salary",
            20,
            True,
            False,
            False,
            360.0,
        ),  # (C1=T, C2=T) or ... -> Rezultat: T
        (
            4000,
            "salary",
            30,
            True,
            False,
            False,
            400.0,
        ),  # (C1=F, C2=T) or ... -> Rezultat: F
        (
            6000,
            "salary",
            20,
            True,
            False,
            False,
            600.0,
        ),  # (C1=T, C2=F) or ... -> Rezultat: F
        (
            6000,
            "salary",
            30,
            False,
            False,
            False,
            540.0,
        ),  # ... or (C3=T, C4=T) -> Rezultat: T
        (
            6000,
            "salary",
            30,
            True,
            False,
            False,
            600.0,
        ),  # ... or (C3=F, C4=T) -> Rezultat: F
        (
            6000,
            "crypto",
            30,
            False,
            False,
            False,
            900.0,
        ),  # ... or (C3=T, C4=F) -> Rezultat: F
        # --- MC/DC: age >= 65 (C1) and income <= 30000 (C2) ---
        (20000, "salary", 70, True, False, False, 2000.0),  # C1=T, C2=T -> Rezultat: T
        (20000, "salary", 30, True, False, False, 2500.0),  # C1=F, C2=T -> Rezultat: F
        # --- MC/DC: age >= 65 (C1) and income > 30000 (C2) ---
        (40000, "salary", 70, True, False, False, 4675.0),  # C1=T, C2=T -> Rezultat: T
        (40000, "salary", 30, True, False, False, 5500.0),  # C1=F, C2=T -> Rezultat: F
        (10000, "salary", 70, True, False, False, 800.0),  # C1=T, C2=F -> Rezultat: F
        # --- MC/DC: is_married (C1) and has_dependents (C2) and income < 80000 (C3) ---
        (
            50000,
            "business",
            40,
            True,
            True,
            True,
            10625.0,
        ),  # C1=T, C2=T, C3=T -> Rezultat: T
        (
            50000,
            "business",
            40,
            True,
            True,
            False,
            12500.0,
        ),  # C1=F, C2=T, C3=T -> Rezultat: F
        (
            100000,
            "business",
            40,
            True,
            True,
            True,
            25000.0,
        ),  # C1=T, C2=T, C3=F -> Rezultat: F
        # --- MC/DC: is_married (C1) and not has_dependents (C2) ---
        (
            50000,
            "business",
            40,
            True,
            False,
            True,
            11875.0,
        ),  # C1=T, C2=T -> Rezultat: T
        (
            50000,
            "business",
            40,
            True,
            False,
            False,
            12500.0,
        ),  # C1=F, C2=T -> Rezultat: F
        (
            100000,
            "business",
            40,
            True,
            True,
            True,
            25000.0,
        ),  # C1=T, C2=F -> Rezultat: F
    ],
)
def test_condition_coverage(
    engine, income, category, age, is_resident, has_dependents, is_married, expected
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
