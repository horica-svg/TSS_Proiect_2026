import pytest

from tests.structural_coverage.helpers import assert_tax_case


@pytest.mark.parametrize(
    "income, category, age, is_resident, has_dependents, is_married, expected",
    [
        # --- Validari initiale ---
        ("a", "salary", 20, True, False, False, "Error: Invalid Data Type"),
        (-1, "salary", 20, True, False, False, "Error: Invalid Income"),
        (3000, "salary", -1, True, False, False, "Error: Invalid Age"),
        (3000, "salari", 20, True, False, False, "Error: Invalid Category"),
        # --- Categoria Salary si Deduceri standard ---
        # Acopera if income <= 10000 si reducere tineri < 25
        (3000, "salary", 20, True, False, False, 270.0),
        # Acopera reducere seniori venit mic
        (20000, "salary", 70, True, False, False, 2000.0),
        # Acopera reducere seniori venit mare
        (60000, "salary", 70, True, False, False, 7650.0),
        # Acopera deducere familie completa
        (40000, "salary", 35, True, True, True, 4675.0),
        # Acopera deducere casatorit fara copii
        (40000, "salary", 35, True, False, True, 5225.0),
        # --- Categoria Business ---
        # Acopera elif income < 20000
        (10000, "business", 40, True, False, False, 2000.0),
        # Acopera if income > 200000
        (250000, "business", 40, True, False, False, 65000.0),
        # Business normal -> Sare peste ambele if-uri de reducere/taxare extra
        (100000, "business", 40, True, False, False, 25000.0),
        # --- Categoria Investment ---
        # Acopera elif income < 5000
        (3000, "investment", 40, True, False, False, 382.5),
        # Acopera if income > 100000
        (150000, "investment", 40, True, False, False, 24000.0),
        # Investment normal -> Sare peste ambele if-uri
        (50000, "investment", 40, True, False, False, 7500.0),
        # --- Categoria Freelance ---
        # Acopera taxare extra pentru rezidenti > 50000
        (60000, "freelance", 40, True, False, False, 8000.0),
        # Critic: forteaza intrarea pe liniile cu tax -= 500 si if tax < 0: tax = 0
        (1000, "freelance", 40, True, True, False, 0.0),
        # Freelance normal -> Sare peste if-ul de rezidenta si if-ul de dependenti
        (40000, "freelance", 40, True, False, False, 4800.0),
        # --- Categoria Crypto ---
        # Acopera if income > 10000 si if not is_resident
        (15000, "crypto", 40, False, False, False, 3750.0),
        # Crypto normal -> Sare peste supra-taxare si penalizare non-rezident
        (5000, "crypto", 40, True, False, False, 500.0),
        # --- Categoria Real Estate ---
        # Acopera if income <= 50000
        (40000, "real_estate", 40, True, False, False, 2000.0),
        # Acopera elif 50000 < income <= 100000
        (75000, "real_estate", 40, True, False, False, 5000.0),
        # Acopera else-ul final
        (150000, "real_estate", 40, True, False, False, 17500.0),
        # --- Corectii pentru Branch Coverage (Acoperire 100%) ---
        # Casatorit, cu dependenti, dar venit mare. Pica IF si ELIF de familie.
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
