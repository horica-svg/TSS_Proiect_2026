from typing import Union

try:
    from App.cli_args import parse_cli_arguments
except ModuleNotFoundError:
    from cli_args import parse_cli_arguments


class TaxEngine:
    def __init__(self):
        self.min_income = 0
        self.max_income = 1000000
        self.min_age = 0
        self.max_age = 150
        self.valid_categories = {
            "salary",
            "business",
            "investment",
            "freelance",
            "crypto",
            "real_estate",
        }

    def calculate_annual_tax(
        self,
        income: Union[int, float],
        category: str,
        age: int,
        is_resident: bool,
        has_dependents: bool = False,
        is_married: bool = False,
    ):
        # 1. Validare date (Clase de echivalenta)
        if not isinstance(income, (int, float)) or not isinstance(age, int):
            return "Error: Invalid Data Type"

        if income < self.min_income or income > self.max_income:
            return "Error: Invalid Income"

        if age < self.min_age or age > self.max_age:
            return "Error: Invalid Age"

        if category not in self.valid_categories:
            return "Error: Invalid Category"

        tax = 0
        # 2. Logica pe categorii (Decizii multiple)
        if category == "salary":
            # Praguri de impozitare (Valori de frontieră)
            if income <= 10000:
                tax = income * 0.1
            elif income > 10000 and income <= 50000:
                tax = 1000 + (income - 10000) * 0.15
            else:
                tax = 7000 + (income - 50000) * 0.2
        elif category == "business":
            tax = income * 0.25
            if income > 200000:
                tax += (income - 200000) * 0.05  # Tax suplimentar pentru venituri mari
            elif income < 20000:
                tax = tax * 0.8  # Reducere de 20% pentru venituri mici
        elif category == "investment":
            tax = income * 0.15
            if income > 100000:
                tax += (income - 100000) * 0.03  # Tax suplimentar pentru venituri mari
            elif income < 5000:
                tax = tax * 0.85  # Reducere de 15% pentru venituri mici
        elif category == "freelance":
            tax = income * 0.12
            if income >= 50000 and is_resident:
                tax += (income - 50000) * 0.08
            if has_dependents:
                tax -= 500  # Deducere fixa pentru dependenti
                tax = max(0, tax)
        elif category == "crypto":
            tax = income * 0.10
            if income > 10000:
                tax += (
                    income - 10000
                ) * 0.20  # Supra-taxare pentru castiguri mari din crypto
            if not is_resident:
                tax = (
                    tax * 1.5
                )  # Penalizare pentru non-rezidenti care tranzactioneaza crypto in tara
        elif category == "real_estate":
            if income <= 50000:
                tax = income * 0.05
            elif 50000 < income <= 100000:
                tax = 2500 + (income - 50000) * 0.10
            else:
                tax = 7500 + (income - 100000) * 0.20

        # 3. Deduceri cu conditii compuse (Acoperire Conditie/Decizie/MC-DC)
        if (age < 25 and income < 5000) or (not is_resident and category != "crypto"):
            tax = tax * 0.9  # Reducere de 10%
        elif age >= 65 and income <= 30000:
            tax = tax * 0.80  # Reducere de 20% pentru seniori cu venit mic
        elif age >= 65 and income > 30000:
            tax = tax * 0.85  # Reducere de 15% standard pentru seniori

        # 4. Conditii de familie (Oportunitati extra de teste)
        if is_married and has_dependents and income < 80000:
            tax = tax * 0.85  # Deducere compusa pentru familii
        elif is_married and not has_dependents:
            tax = tax * 0.95  # Deducere mica pentru casatoriti fara dependenti

        if tax < 0:
            tax = 0  # Evitarea taxelor negative

        return round(tax, 2)


def main() -> None:
    args = parse_cli_arguments()

    engine = TaxEngine()
    result = engine.calculate_annual_tax(
        income=args.income,
        category=args.category,
        age=args.age,
        is_resident=args.resident,
        has_dependents=args.dependents,
        is_married=args.married,
    )
    print(result)


if __name__ == "__main__":
    main()
