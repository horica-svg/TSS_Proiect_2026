import pytest

from tests.structural_coverage.helpers import assert_tax_case


@pytest.mark.parametrize(
    "income,category,age,is_resident,has_dependents,is_married,expected",
    [
        (4000, "salary", 24, True, False, False, 360.0),
        (4000, "salary", 26, False, False, False, 360.0),
        (4000, "crypto", 26, False, False, False, 600.0),
        (30000, "salary", 65, True, False, False, 3200.0),
    ],
)
def test_condition_coverage(
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
