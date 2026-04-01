from csv import Error
import pytest

from App.Tax_Calculator import TaxEngine


def assert_tax_case(
    engine,
    income,
    category,
    age,
    is_resident,
    has_dependents=False,
    is_married=False,
    *,
    expected,
):
    result = engine.calculate_annual_tax(
        income=income,
        category=category,
        age=age,
        is_resident=is_resident,
        has_dependents=has_dependents,
        is_married=is_married,
    )
    assert result == expected


# Student 3 (explicit) - Structural Coverage / White-Box
@pytest.fixture
def engine():
    return TaxEngine()


@pytest.mark.parametrize(
    "income, category, age, is_resident, has_dependents, is_married, expected",
    [
        # --- Validări inițiale ---
        ("a", "salary", 20, True, False, False, "Error: Invalid Data Type"),
        (-1, "salary", 20, True, False, False, "Error: Invalid Income"),
        (3000, "salary", -1, True, False, False, "Error: Invalid Age"),
        (3000, "salari", 20, True, False, False, "Error: Invalid Category"),
        # --- Categoria Salary și Deduceri standard ---
        # Acoperă if income <= 10000 și reducere tineri < 25
        (3000, "salary", 20, True, False, False, 270.0),
        # Acoperă reducere seniori venit mic
        (20000, "salary", 70, True, False, False, 2000.0),
        # Acoperă reducere seniori venit mare
        (60000, "salary", 70, True, False, False, 7650.0),
        # Acoperă deducere familie completă
        (40000, "salary", 35, True, True, True, 4675.0),
        # Acoperă deducere căsătorit fără copii
        (40000, "salary", 35, True, False, True, 5225.0),
        # --- Categoria Business ---
        # Acoperă elif income < 20000
        (10000, "business", 40, True, False, False, 2000.0),
        # Acoperă if income > 200000
        (250000, "business", 40, True, False, False, 65000.0),
        # Business normal -> Sare peste ambele if-uri de reducere/taxare extra
        (100000, "business", 40, True, False, False, 25000.0),
        # --- Categoria Investment ---
        # Acoperă elif income < 5000
        (3000, "investment", 40, True, False, False, 382.5),
        # Acoperă if income > 100000
        (150000, "investment", 40, True, False, False, 24000.0),
        # Investment normal -> Sare peste ambele if-uri
        (50000, "investment", 40, True, False, False, 7500.0),
        # --- Categoria Freelance ---
        # Acoperă taxare extra pentru rezidenți > 50000
        (60000, "freelance", 40, True, False, False, 8000.0),
        # Critic: forțează intrarea pe liniile cu tax -= 500 și if tax < 0: tax = 0
        (1000, "freelance", 40, True, True, False, 0.0),
        # Freelance normal -> Sare peste if-ul de rezidență și if-ul de dependenți
        (40000, "freelance", 40, True, False, False, 4800.0),
        # --- Categoria Crypto ---
        # Acoperă if income > 10000 și if not is_resident
        (15000, "crypto", 40, False, False, False, 3750.0),
        # Crypto normal -> Sare peste supra-taxare și penalizare non-rezident
        (5000, "crypto", 40, True, False, False, 500.0),
        # --- Categoria Real Estate ---
        # Acoperă if income <= 50000
        (40000, "real_estate", 40, True, False, False, 2000.0),
        # Acoperă elif 50000 < income <= 100000
        (75000, "real_estate", 40, True, False, False, 5000.0),
        # Acoperă else-ul final
        (150000, "real_estate", 40, True, False, False, 17500.0),
        # --- Corecții pentru Branch Coverage (Acoperire 100%) ---
        # Căsătorit, cu dependenți, dar venit mare. Pică IF și ELIF de familie.
        (100000, "salary", 40, True, True, True, 17000.0),
    ],
)
def test_statement_coverage(
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


@pytest.mark.parametrize(
    "income,category,age,is_resident,has_dependents,is_married,expected",
    [
        (18000, "business", 35, True, False, False, 3600.0),
        (250000, "business", 35, True, False, False, 65000.0),
        (49000, "freelance", 35, True, True, False, 5380.0),
        (51000, "freelance", 35, True, False, False, 6200.0),
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


@pytest.mark.parametrize(
    "income,category,age,is_resident,has_dependents,is_married,expected",
    [
        (4000, "salary", 24, True, False, False, 360.0),
        (4000, "salary", 26, False, False, False, 360.0),
        (4000, "crypto", 26, False, False, False, 600.0),
        (30000, "salary", 65, True, False, False, 3200.0),
    ],
)
def test_condition_coverage_mcdc_focus(
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


@pytest.mark.parametrize(
    "income,category,age,is_resident,has_dependents,is_married,expected",
    [
        (10000, "salary", 30, True, False, False, 1000.0),
        (10000, "salary", 30, False, False, False, 900.0),
        (70000, "salary", 30, True, True, True, 9350.0),
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
