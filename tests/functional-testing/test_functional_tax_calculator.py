import unittest 

from App.Tax_Calculator import TaxEngine

class TestFunctionalTaxCalculator(unittest.TestCase) :
    def setUp(self):
        self.engine = TaxEngine()

    def test_invalid_data_types(self):
        # testam tipuri de date incorecte pentru income si age
        self.assertEqual(self.engine.calculate_annual_tax("1000", "salary", 30, True), "Error: Invalid Data Type")
        self.assertEqual(self.engine.calculate_annual_tax(1000, "salary", "30", True), "Error: Invalid Data Type")

    def test_invalid_income_boundaries(self):
        # limite pentru income: 0 - 1000000, testam exact in afara lor.
        self.assertEqual(self.engine.calculate_annual_tax(-1, "salary", 30, True), "Error: Invalid Income")
        self.assertEqual(self.engine.calculate_annual_tax(1000001, "salary", 30, True), "Error: Invalid Income")

    def test_invalid_age_boundaries(self):
        # limite pentru age: 0 - 150, testam exact in afara lor.
        self.assertEqual(self.engine.calculate_annual_tax(50000, "salary", -1, True), "Error: Invalid Age")
        self.assertEqual(self.engine.calculate_annual_tax(50000, "salary", 151, True), "Error: Invalid Age")

    def test_invalid_category(self):
        # testam o categorie care nu este in valid_categories
        self.assertEqual(self.engine.calculate_annual_tax(50000, "unknown_category", 30, True), "Error: Invalid Category")


    def test_salary_first_bracket(self):
        # interval:<= 10000. taxa:10%
        # testam valoare normala si valoare exact pe limita
        self.assertEqual(self.engine.calculate_annual_tax(5000, "salary", 30, True), 500.0)
        self.assertEqual(self.engine.calculate_annual_tax(10000, "salary", 30, True), 1000.0)

    def test_salary_second_bracket(self):
        # interval: 10001 - 50000. taxa:1000+(income-10000)*0.15
        # valoare normala(30000): 1000+20000*0.15=4000
        self.assertEqual(self.engine.calculate_annual_tax(30000, "salary", 30, True), 4000.0)
        # limita de sus(50000): 1000+40000*0.15=7000
        self.assertEqual(self.engine.calculate_annual_tax(50000, "salary", 30, True), 7000.0)

    def test_salary_third_bracket(self):
        # interval: > 50000. taxa:7000+(income-50000)*0.2
        # valoare(100000): 7000+50000*0.2=17000
        self.assertEqual(self.engine.calculate_annual_tax(100000, "salary", 30, True), 17000.0)

    def test_freelance_with_dependents(self):
        # interval: income = 10000. taxa de baza:10000*0.12=1200
        # deducere dependenti:1200-500=700
        self.assertEqual(self.engine.calculate_annual_tax(10000, "freelance", 30, True, has_dependents=True), 700.0)

    def test_crypto_non_resident_penalty(self):
        # interval: income = 5000. taxa de baza:5000*0.10=500
        # penalizare non-rezident: 500*1.5=750
        self.assertEqual(self.engine.calculate_annual_tax(5000, "crypto", 30, is_resident=False), 750.0)


    # --- 4. teste pt deduceri compuse (varsta, stare civila) ---

    def test_discount_young_low_income(self):
        # varsta < 25, venit < 5000. categorie 'salary'.
        # taxa de baza: 4000*0.10=400. reducere 10%:400*0.9=360
        self.assertEqual(self.engine.calculate_annual_tax(4000, "salary", 20, True), 360.0)

    def test_discount_senior_low_income(self):
        # varsta >= 65, venit <= 30000. categorie 'salary'.
        # taxa de baza la 20000 (bracket 2): 1000+10000*0.15=2500
        # reducere 20%:2500*0.8=2000
        self.assertEqual(self.engine.calculate_annual_tax(20000, "salary", 65, True), 2000.0)

    def test_discount_married_with_dependents(self):
        # casatorit,cu dependenti, venit < 80000. categorie 'salary', nu prinde alte reduceri de varsta.
        # venit:40000. taxa de baza:1000+30000*0.15=5500
        # reducere familii:5500*0.85=4675
        self.assertEqual(self.engine.calculate_annual_tax(40000, "salary", 40, True, has_dependents=True, is_married=True), 4675.0)


    def test_business_brackets(self):
        # venit mic < 20000. venit:10000. taxa:10000*0.25=2500. reducere 20%:2500*0.8=2000
        self.assertEqual(self.engine.calculate_annual_tax(10000, "business", 40, True), 2000.0)
        # venit normal. venit:100000. taxa:100000*0.25=25000
        self.assertEqual(self.engine.calculate_annual_tax(100000, "business", 40, True), 25000.0)
        # venit mare > 200000. venit:300000. taxa:300000*0.25=75000. extra:(300000-200000)*0.05=5000. total:80000
        self.assertEqual(self.engine.calculate_annual_tax(300000, "business", 40, True), 80000.0)

    def test_investment_brackets(self):
        # venit mic < 5000. venit:4000. taxa:4000*0.15=600. reducere 15%:600*0.85=510
        self.assertEqual(self.engine.calculate_annual_tax(4000, "investment", 40, True), 510.0)
        # venit normal.venit:50000. taxa:50000*0.15=7500
        self.assertEqual(self.engine.calculate_annual_tax(50000, "investment", 40, True), 7500.0)
        # venit mare> 100000. venit:150000. taxa:150000*0.15=22500. extra:(150000-100000)*0.03=1500. total:24000
        self.assertEqual(self.engine.calculate_annual_tax(150000, "investment", 40, True), 24000.0)

    def test_other_category_brackets(self):
        # intra pe ramura 'else'(ex: real_estate)
        # <= 50000. taxa:5%
        self.assertEqual(self.engine.calculate_annual_tax(40000, "real_estate", 40, True), 2000.0)
        # > 50000 si <= 100000. taxa:2500+(income-50000)*0.10
        self.assertEqual(self.engine.calculate_annual_tax(80000, "real_estate", 40, True), 5500.0)
        # > 100000. taxa:7500+(income-100000)*0.20
        self.assertEqual(self.engine.calculate_annual_tax(150000, "real_estate", 40, True), 17500.0)