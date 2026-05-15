import pytest

from tests.structural_coverage.helpers import assert_tax_case


@pytest.mark.parametrize(
    "income, category, age, is_resident, has_dependents, is_married, expected",
    [
        # --- Validări inițiale (Erori) ---
        ("a", "salary", 20, True, False, False, "Error: Invalid Data Type"),  # Path: N1->N2->N3
        (-1, "salary", 20, True, False, False, "Error: Invalid Income"),     # Path: N1->N2->N4->N5
        (3000, "salary", -1, True, False, False, "Error: Invalid Age"),      # Path: N1->N2->N4->N6->N7
        (3000, "salari", 20, True, False, False, "Error: Invalid Category"), # Path: N1->N2->N4->N6->N8->N9

        # --- Categorii + Ajustări (Căi de succes) ---
        # Salary <= 10k, age < 25 & income < 5k (10% ded), not married
        (4000, "salary", 20, True, False, False, 360.0), 
        # Path: N1->N2->N4->N6->N8->N10->N11->N12->N18->N20->N25->N27->N29->N31

        # 10k < salary <= 50k, not senior, not married
        (3000, "salary", 30, True, False, False, 300.0), 
        # Path: N1->N2->N4->N6->N8->N10->N11->N12->N18->N21->N23->N25->N27->N29->N31

        # Salary > 50k, not senior, not married
        (80000, "salary", 40, True, False, False, 13000.0),
        # Path: N1->N2->N4->N6->N8->N10->N11->N12->N18->N21->N23->N25->N27->N29->N31

        # Business > 200k, not senior, not married
        (300000, "business", 30, True, False, False, 80000.0),
        # Path: N1->N2->N4->N6->N8->N10->N11->N13->N18->N21->N23->N25->N27->N29->N31

        # 20k <= business <= 200k, not senior, not married
        (100000, "business", 35, True, False, False, 25000.0),
        # Path: N1->N2->N4->N6->N8->N10->N11->N13->N18->N21->N23->N25->N27->N29->N31

        # Business < 20k, not senior, not married
        (15000, "business", 25, True, False, False, 3000.0),
        # Path: N1->N2->N4->N6->N8->N10->N11->N13->N18->N21->N23->N25->N27->N29->N31

        # Investment < 5k, age 30, resident, not married
        (4000, "investment", 30, True, False, False, 510.0),
        # Path: N1->N2->N4->N6->N8->N10->N11->N14->N18->N21->N23->N25->N27->N29->N31

        # Investment > 100k, not senior, not married
        (200000, "investment", 45, True, False, False, 33000.0),
        # Path: N1->N2->N4->N6->N8->N10->N11->N14->N18->N21->N23->N25->N27->N29->N31

        # Freelance >= 50k, resident, married + dep + income < 80k (15% ded)
        (60000, "freelance", 30, True, True, True, 6375.0),
        # Path: N1->N2->N4->N6->N8->N10->N11->N15->N18->N21->N23->N25->N26->N29->N31

        # Freelance < 50k, age 25, resident, not married
        (30000, "freelance", 25, True, False, False, 3600.0),
        # Path: N1->N2->N4->N6->N8->N10->N11->N15->N18->N21->N23->N25->N27->N29->N31

        # Freelance, not resident (10% ded section 3), not married
        (60000, "freelance", 40, False, False, False, 6480.0),
        # Path: N1->N2->N4->N6->N8->N10->N11->N15->N18->N20->N25->N27->N29->N31

        # Crypto > 10k, not resident (not crypto for deduction? check code)
        # Note: (not is_resident and category != "crypto") -> Crypto non-resident DOES NOT get 10% reduction in section 3
        (50000, "crypto", 30, False, False, False, 19500.0),
        # Path: N1->N2->N4->N6->N8->N10->N11->N16->N18->N21->N23->N25->N27->N29->N31

        # Crypto <= 10k, resident, not married
        (5000, "crypto", 30, True, False, False, 500.0),
        # Path: N1->N2->N4->N6->N8->N10->N11->N16->N18->N21->N23->N25->N27->N29->N31

        # Real Estate 50k-100k, married no dependents (5% ded section 4)
        (70000, "real_estate", 40, True, False, True, 4275.0),
        # Path: N1->N2->N4->N6->N8->N10->N11->N17->N18->N21->N23->N25->N27->N28->N29->N31

        # Real Estate <= 50k, not senior, not married
        (30000, "real_estate", 35, True, False, False, 1500.0),
        # Path: N1->N2->N4->N6->N8->N10->N11->N17->N18->N21->N23->N25->N27->N29->N31

        # Real Estate > 100k, not senior, not married
        (150000, "real_estate", 50, True, False, False, 17500.0),
        # Path: N1->N2->N4->N6->N8->N10->N11->N17->N18->N21->N23->N25->N27->N29->N31

        # Senior, income <= 30k (20% ded section 3)
        (20000, "salary", 70, True, False, False, 2000.0),
        # Path: N1->N2->N4->N6->N8->N10->N11->N12->N18->N21->N22->N25->N27->N29->N31

        # Senior, income > 30k (15% ded section 3)
        (40000, "salary", 70, True, False, False, 4675.0),
        # Path: N1->N2->N4->N6->N8->N10->N11->N12->N18->N21->N23->N24->N25->N27->N29->N31

        # Married + dependents, income >= 80k (No deduction in section 4)
        (100000, "salary", 40, True, True, True, 17000.0),
        # Path: N1->N2->N4->N6->N8->N10->N11->N12->N18->N21->N23->N25->N26? (No, income < 80k check) -> N25->N27->N29->N31
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


def test_independent_paths_circuit_p25_forced(engine, monkeypatch):
    # P25 este infezabil in flux normal; forțam max(0, tax) sa lase valoarea negativa.
    monkeypatch.setattr("builtins.max", lambda _min_value, current_tax: current_tax)

    result = engine.calculate_annual_tax(
        income=1000,
        category="freelance",
        age=30,
        is_resident=True,
        has_dependents=True,
        is_married=False,
    )

    # Ramura finala P25 (tax < 0) normalizeaza rezultatul la 0.
    assert result == 0
