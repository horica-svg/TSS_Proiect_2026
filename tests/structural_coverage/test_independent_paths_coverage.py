import pytest

from tests.structural_coverage.helpers import assert_tax_case


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
