import pytest

from tests.structural_coverage.helpers import assert_tax_case


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
