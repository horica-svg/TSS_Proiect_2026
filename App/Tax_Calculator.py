class TaxEngine:
    def __init__(self):
        self.min_income = 0
        self.max_income = 1000000

    def calculate_annual_tax(self, income, category, age, is_resident):
        if income < self.min_income or income > self.max_income:
            return "Error: Invalid Income"
        
        tax = 0
        if category == "salary":
            if income <= 10000:
                tax = income * 0.1
            elif income > 10000 and income <= 50000:
                tax = 1000 + (income - 10000) * 0.15
            else:
                tax = 7000 + (income - 50000) * 0.2
        elif category == "business":
            tax = income * 0.25
            if income > 200000:
                tax += (income - 200000) * 0.05 
            elif income < 20000:
                tax = tax * 0.8
        elif category == "investment":
            tax = income * 0.15
            if income > 100000:
                tax += (income - 100000) * 0.03
            elif income < 5000:
                tax = tax * 0.85
        else:
            return "Error: Invalid Category"
        
        
        if (age < 25 and income < 5000) or not is_resident:
            tax = tax * 0.9 
        elif age > 65:
            tax = tax * 0.85
                    
        return round(tax, 2)