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
