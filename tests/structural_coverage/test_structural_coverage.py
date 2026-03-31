import pytest

from tests.test_helpers import assert_tax_case, create_engine


# Student 3 (explicit) - Structural Coverage / White-Box
@pytest.fixture
def engine():
    return create_engine()


@pytest.mark.parametrize(
    "income,category,age,is_resident,expected,has_dependents,is_married",
    [
        (3000, "salary", 20, True, 270.0, False, False),
        (20000, "salary", 70, True, 2000.0, False, False),
        (60000, "salary", 70, True, 7650.0, False, False),
        (40000, "salary", 35, True, 4675.0, True, True),
        (40000, "salary", 35, True, 5225.0, False, True),
    ],
)
def test_statement_coverage(
    engine,
    income,
    category,
    age,
    is_resident,
    expected,
    has_dependents,
    is_married,
):
    assert_tax_case(
        engine,
        income,
        category,
        age,
        is_resident,
        expected,
        has_dependents,
        is_married,
    )


@pytest.mark.parametrize(
    "income,category,age,is_resident,expected,has_dependents,is_married",
    [
        (18000, "business", 35, True, 3600.0, False, False),
        (250000, "business", 35, True, 65000.0, False, False),
        (49000, "freelance", 35, True, 5380.0, True, False),
        (51000, "freelance", 35, True, 6200.0, False, False),
    ],
)
def test_branch_coverage(
    engine,
    income,
    category,
    age,
    is_resident,
    expected,
    has_dependents,
    is_married,
):
    assert_tax_case(
        engine,
        income,
        category,
        age,
        is_resident,
        expected,
        has_dependents,
        is_married,
    )


@pytest.mark.parametrize(
    "income,category,age,is_resident,expected,has_dependents,is_married",
    [
        (4000, "salary", 24, True, 360.0, False, False),
        (4000, "salary", 26, False, 360.0, False, False),
        (4000, "crypto", 26, False, 600.0, False, False),
        (30000, "salary", 65, True, 3200.0, False, False),
    ],
)
def test_condition_coverage_mcdc_focus(
    engine,
    income,
    category,
    age,
    is_resident,
    expected,
    has_dependents,
    is_married,
):
    assert_tax_case(
        engine,
        income,
        category,
        age,
        is_resident,
        expected,
        has_dependents,
        is_married,
    )


@pytest.mark.parametrize(
    "income,category,age,is_resident,expected,has_dependents,is_married",
    [
        (10000, "salary", 30, True, 1000.0, False, False),
        (10000, "salary", 30, False, 900.0, False, False),
        (70000, "salary", 30, True, 9350.0, True, True),
    ],
)
def test_independent_paths_circuits(
    engine,
    income,
    category,
    age,
    is_resident,
    expected,
    has_dependents,
    is_married,
):
    assert_tax_case(
        engine,
        income,
        category,
        age,
        is_resident,
        expected,
        has_dependents,
        is_married,
    )
