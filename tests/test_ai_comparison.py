import pytest
from App.Tax_Calculator import calculate_tax


@pytest.mark.parametrize(
    "scenario, freelance_income, expenses, expected_tax",
    [
        ("Lower boundary", 0, 0, 0.0),
        ("Standard Freelance Logic (AI Assumption: 10%)", 15000, 5000, 1000.0),
        ("High Income Logic (AI Assumption: 10%)", 40000, 10000, 3000.0),
        ("Invalid negative income", -5000, 0, ValueError),
    ],
)
def test_freelance_tax_ai_generated(scenario, freelance_income, expenses, expected_tax):
    """
    Test generat de AI bazat pe analiza claselor de echivalenta.
    AI-ul a dedus gresit o taxa liniara de 10% din profit.
    """
    if expected_tax == ValueError:
        with pytest.raises(ValueError):
            calculate_tax(freelance_income=freelance_income, business_expenses=expenses)
    else:
        result = calculate_tax(
            freelance_income=freelance_income, business_expenses=expenses
        )
        assert result == expected_tax
