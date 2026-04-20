# Mutation Analysis

Am utilizat tehnica **Mutation Testing** pentru a evalua eficienta setului de teste functionale. Am generat mai multi mutanti de primul ordin prin modificari sintactice minime, apoi am rulat suita de teste pentru a observa daca acestea sunt omorate sau raman nedetectate.

* In urma analizei manuale am obtinut un scor al mutantilor de *16 / 22 = 0.7272*, adica testele detecteaza aproximativ 73% din mutantii generati.

Pentru a confirma acest scor, am decis sa folosesc si un tool de automatizare al mutantilor: *mutmut*.

* Scorul obtinut folosind mutmut a fost de *181 / 228 = 0.7930*, asemanator cu analiza manuala.

In urma executarii **mutmut run**, biblioteca se ocupa de generarea mutantilor si rularea testelor.
```bash
claudiu@Lenovo:~/projects/TSS_Proiect_2026$ mutmut run
⠦ Generating mutants
    done in 2597ms (1 files mutated, 0 ignored, 0 unmodified)
⠼ Running stats     
    done
⠼ Running clean tests
    done
⠋ Running forced fail test
    done
Running mutation testing
⠏ 228/228  🎉 181 🫥 0  ⏰ 0  🤔 0  🙁 47  🔇 0  🧙 0
33.49 mutations/second
```

Rezultatele mutmut:
```bash
App.Tax_Calculator.xǁTaxEngineǁ__init____mutmut_2: survived
App.Tax_Calculator.xǁTaxEngineǁ__init____mutmut_6: survived
App.Tax_Calculator.xǁTaxEngineǁcalculate_annual_tax__mutmut_1: survived
App.Tax_Calculator.xǁTaxEngineǁcalculate_annual_tax__mutmut_2: survived
App.Tax_Calculator.xǁTaxEngineǁcalculate_annual_tax__mutmut_10: survived
App.Tax_Calculator.xǁTaxEngineǁcalculate_annual_tax__mutmut_11: survived
App.Tax_Calculator.xǁTaxEngineǁcalculate_annual_tax__mutmut_16: survived
...
```

Pentru a vedea detalii despre un mutant, se poate rula comanda **mutmut show < id>**:
```bash 
@@ -14,7 +14,7 @@
     if income < self.min_income or income > self.max_income:
         return "Error: Invalid Income"
 
-    if age < self.min_age or age > self.max_age:
+    if age < self.min_age or age >= self.max_age:
         return "Error: Invalid Age"
 
     if category not in self.valid_categories:
```

## 1. Rezultatele Analizei Manuale

### Valori de Frontiera

| Categorie | Tipul Mutatiei | Modificare | Status | Tip Mutant |
| :--- | :--- | :--- | :--- | :--- |
| **Salary** | Mutatie de Inlocuire & Valori de Frontiera | `income <= 10000` -> `income < 10000` | **Omorat** | Ordin 1 |
| **Business** | Mutatie de Inlocuire & Valori de Frontiera | `income > 200000` -> `income >= 200000` | **Supravietuit** | Echivalent |
| **Investment** | Mutatie de Inlocuire & Valori de Frontiera | `income < 5000` -> `income <= 5000` | **Supravietuit** | Neacoperit |
| **Freelance** | Mutatie de Inlocuire & Valori de Frontiera | `income > 50000` -> `income >= 50000` | **Supravietuit** | Neacoperit |
| **Crypto** | Mutatie de Inlocuire & Valori de Frontiera | `income > 10000` -> `income >= 10000` | **Supravietuit** | Echivalent |
| **Others** | Mutatie de Inlocuire & Valori de Frontiera | `income <= 50000` -> `income < 50000` | **Supravietuit** | Neacoperit |

### Mutanti specifici categoriei Freelance

| Categorie | Tipul Mutatiei | Modificare | Status | Tip Mutant |
| :--- | :--- | :--- | :--- | :--- |
| **Freelance_M2** | Mutatie de Stergere | Eliminat `tax = max(0,tax)` | **Supravietuit** | Neacoperit |
| **Freelance_M3** | Modificare Constanta | `tax -= 500` -> `tax -= 499` | **Omorat** | Ordin 1 |
| **Freelance_M4** | Mutatie de Stergere | Eliminat `if has_dependents` | **Omorat** | Ordin 1 |
| **Freelance_M5** | Modificare Constanta | `tax = income * 0.12` -> `tax = income * 0.18` | **Omorat** | Ordin 1 |
| **Freelance_M6** | Mutatie de Inlocuire | `and` -> `or` in `if income >= 50000 _ is_resident` | **Omorat** | Ordin 1 |

### Mutanti specifici categoriei Crypto

| Categorie | Tipul Mutatiei | Modificare | Status | Tip Mutant |
| :--- | :--- | :--- | :--- | :--- |
| **Crypto_M2** | Mutatie de Inlocuire | `if not is_resident` -> `if is_resident` | **Omorat** | Ordin 1 |
| **Crypto_M3** | Modificare Constanta | `tax = income * 0.10` -> `tax = income * 0.11` | **Omorat** | Ordin 1 |
| **Crypto_M4** | Modificare Constanta | `tax = ( tax * 1.5 )` -> `tax = ( tax * 1.9 )` | **Omorat** | Ordin 1 |

### Deductii

| Categorie | Tipul Mutatiei | Modificare | Status | Tip Mutant |
| :--- | :--- | :--- | :--- | :--- |
| **Deductions_M1** | Mutatie de Inlocuire | `(not is_resident and category != "crypto")` -> `(not is_resident or category != "crypto")` | **Omorat** | Ordin 1 |
| **Deductions_M2** | Mutatie de Inlocuire | `(age < 25 and income < 5000)` -> `(age < 25 or income < 5000)` | **Omorat** | Ordin 1 |
| **Deductions_M3** | Mutatie de Inlocuire | `elif age >= 65 and income <= 30000` -> `elif age > 65 and income <= 30000` | **Omorat** | Ordin 1 |
| **Deductions_M4** | Modificare Constanta | `tax = tax * 0.9` -> `tax = tax * 0.7` | **Omorat** | Ordin 1 |

### Conditii de Familie

| Categorie | Tipul Mutatiei | Modificare | Status | Tip Mutant |
| :--- | :--- | :--- | :--- | :--- |
| **Family_Conditions_M1** | Mutatie de Inlocuire | `if is_married and has_dependents and income < 80000` -> `if is_married and has_dependents or income < 80000` | **Omorat** | Ordin 1 |
| **Family_Conditions_M2** | Mutatie de Inlocuire | `elif is_married and not has_dependents` -> `elif is_married and has_dependents:` | **Supravietuit** | Neacoperit |

### Valorile Returnate

| Categorie | Tipul Mutatiei | Modificare | Status | Tip Mutant |
| :--- | :--- | :--- | :--- | :--- |
| **Return_Values_M1** | Modificare Constanta | `return round(tax, 2)` -> `return round(tax, 1)` | **Supravietuit** | Neacoperit |
| **Return_Values_M2** | Modificare Constanta | `return round(tax, 2)` -> `return round(tax + 0.01, 2)` | **Omorat** | Ordin 1 |

## 2. Analiza Mutatiilor

### Valorile de Frontiera

#### mutation_analysis/boundary_values/salary
* **Mutatie:** Am modificat operatorul `income <= 10000` in `income < 10000`.
* **Analiza:** Testul test_salary_first_bracket a esuat, ceea ce demonstreaza ca suita de teste acopera corect frontiera de 10000.
* **Explicatie:** Mutantul a fost omorat, validand calitatea testelor pe acest prag.

#### mutation_analysis/boundary_values/business
* **Mutatie:** Am modificat `income > 200000` in `income >= 200000`.
* **Analiza:** Toate testele au trecut. Acest rezultat indica faptul ca mutantul este echivalent.
* **Explicatie:** La valoarea de 200000, termenul de calcul (income - 200000) devine 0. Comportamentul functiei este identic pentru orice set de date.

#### mutation_analysis/boundary_values/investment
* **Mutatie:** Am modificat `income < 5000` in `income <= 5000`.
* **Analiza:** Mutantul a supravietuit. Desi testele au trecut, comportamentul ar fi trebuit sa difere pentru valoarea 5000.
* **Actiune:** Aceasta indica o lipsa de acoperire a valorii de frontiera 5000 in testele actuale. 

#### mutation_analysis/boundary_values/freelance
* **Mutatie:** Am modificat `income > 50000` in `income >= 50000`.
* **Analiza:** Mutantul a supravietuit. Desi testele au trecut, comportamentul ar fi trebuit sa difere pentru valoarea 50000.
* **Actiune:** Aceasta indica o lipsa de acoperire a valorii de frontiera 50000 in testele actuale. 

#### mutation_analysis/boundary_values/crypto
* **Mutatie:** Am modificat `income > 10000` in `income >= 10000`.
* **Analiza:** Toate testele au trecut. Acest rezultat indica faptul ca mutantul este echivalent.
* **Explicatie:** La valoarea de 10000, taxa suplimentara in P este 0, iar in M este tot 0. Comportamentul functiei este identic.

#### mutation_analysis/boundary_values/others
* **Mutatie:** Am modificat `income <= 50000` in `income < 50000`.
* **Analiza:** Toate testele au trecut. Acest rezultat indica faptul ca mutantul este echivalent.
* **Actiune:** Aceasta indica o lipsa de acoperire a valorii de frontiera 50000 in testele actuale. Pentru income = 50000, taxa in P este 50000 * 0.05 = 2500, iar in M este 7500 + 0. Comportamentul functiei este diferit.

### Logica Aplicatiei

#### Freelance

##### mutation_analysis/freelance_m2
* **Mutatie:** Am eliminat linia `tax = max(0,tax)`.
* **Analiza:** Mutantul a supravietuit. Testele ar fi trebuit sa verifice faptul ca programul nu returneaza valori negative.
* **Actiune:** Aceasta indica o lipsa de acopeire a valorilor negative in testele actuale. 

##### mutation_analysis/freelance_m3
* **Mutatie:** Am modificat constanta `tax -= 499`.
* **Analiza:** Testul `test_freelance_with_dependents` a esuat, ceea ce demonstreaza ca suita de teste este indeajuns pentru a verifica comportamentul aplicatiei.
* **Explicatie:** Mutantul a fost omorat. 

##### mutation_analysis/freelance_m4
* **Mutatie:** Am eliminat if-ul `if has_dependents`.
* **Analiza:** Testul `test_freelance_with_dependents` a esuat, ceea ce demonstreaza ca suita de teste este indeajuns pentru a verifica comportamentul aplicatiei.
* **Explicatie:** Mutantul a fost omorat.

##### mutation_analysis/freelance_m5
* **Mutatie:** Am modificat `tax = income * 0.12` in `tax = income * 0.18`.
* **Analiza:** Testul `test_freelance_with_dependents` a esuat, ceea ce demonstreaza ca suita de teste este indeajuns pentru a verifica comportamentul aplicatiei.
* **Explicatie:** Mutantul a fost omorat.

##### mutation_analysis/freelance_m6
* **Mutatie:** Am modificat `and` in `or` in conditia `if income >= 50000 _ is_resident`.
* **Analiza:** Testul `test_freelance_with_dependents` a esuat, ceea ce demonstreaza ca suita de teste este indeajuns pentru a verifica comportamentul aplicatiei.
* **Explicatie:** Mutantul a fost omorat.

#### Crypto

##### mutation_analysis/crypto_m2
* **Mutatie:** Am modificat if-ul `if not is_resident` -> `if is_resident`.
* **Analiza:** Testul `test_crypto_non_resident_penalty` a esuat, ceea ce demonstreaza ca suita de teste este indeajuns pentru a verifica comportamentul aplicatiei.
* **Explicatie:** Mutantul a fost omorat.

##### mutation_analysis/crypto_m3
* **Mutatie:** Am modificat `tax = income * 0.10` -> `tax = income * 0.11`.
* **Analiza:** Testul `test_crypto_non_resident_penalty` a esuat, ceea ce demonstreaza ca suita de teste este indeajuns pentru a verifica comportamentul aplicatiei.
* **Explicatie:** Mutantul a fost omorat.

##### mutation_analysis/crypto_m4
* **Mutatie:** Am modificat `tax = ( tax * 1.5 )` -> `tax = ( tax * 1.9 )`.
* **Analiza:** Testul `test_crypto_non_resident_penalty` a esuat, ceea ce demonstreaza ca suita de teste este indeajuns pentru a verifica comportamentul aplicatiei.
* **Explicatie:** Mutantul a fost omorat.

#### Deduceri

##### mutation_analysis/deductions/m1
* **Mutatie:** Am modificat `if (age < 25 and income < 5000)` -> ` if (age < 25 or income < 5000)`.
* **Analiza:** Testul `test_investment_brackets` a esuat, ceea ce demonstreaza ca suita de teste este indeajuns pentru a verifica comportamentul aplicatiei.
* **Explicatie:** Mutantul a fost omorat.

##### mutation_analysis/deductions/m2
* **Mutatie:** Am modificat `(not is_resident and category != "crypto")` -> `(not is_resident or category != "crypto")`.
* **Analiza:** Testul `test_salary_third_bracket` a esuat, ceea ce demonstreaza ca suita de teste este indeajuns pentru a verifica comportamentul aplicatiei.
* **Explicatie:** Mutantul a fost omorat.

##### mutation_analysis/deductions/m3
* **Mutatie:** Am modificat `elif age >= 65 and income <= 30000` -> `elif age > 65 and income <= 30000`.
* **Analiza:** Testul `test_discount_senior_low_income` a esuat, ceea ce demonstreaza ca suita de teste este indeajuns pentru a verifica comportamentul aplicatiei.
* **Explicatie:** Mutantul a fost omorat.

##### mutation_analysis/deductions/m4
* **Mutatie:** Am modificat `tax = tax * 0.9` -> `tax = tax * 0.7`.
* **Analiza:** Testul `test_discount_young_low_income` a esuat, ceea ce demonstreaza ca suita de teste este indeajuns pentru a verifica comportamentul aplicatiei.
* **Explicatie:** Mutantul a fost omorat.

#### Conditii de Familie

##### mutation_analysis/family_conditions/m1
* **Mutatie:** Am modificat `if is_married and has_dependents and income < 80000` -> `if is_married and has_dependents or income < 80000`.
* **Analiza:** Testul `test_salary_second_bracket` a esuat, ceea ce demonstreaza ca suita de teste este indeajuns pentru a verifica comportamentul aplicatiei.
* **Explicatie:** Mutantul a fost omorat.

##### mutation_analysis/family_conditions/m2
* **Mutatie:** Am modificat `elif is_married and not has_dependents` -> `elif is_married and has_dependents:`.
* **Analiza:** Mutantul a supravietuit.
* **Actiune:** Acesta indica o lipsa a testelor pentru acest caz specific.

#### Valorile Returnate

##### mutation_analysis/return_value/m1
* **Mutatie:** Am modificat `return round(tax, 2)` -> `return round(tax, 1)`.
* **Analiza:** Mutantul a supravietuit. 
* **Actiune:** Acesta indica faptul ca testele nu ar fi destul de sensibile pentru outputul functiei.

##### mutation_analysis/return_value/m2
* **Mutatie:** Am modificat `return round(tax, 2)` -> `return round(tax + 0.01, 2)`.
* **Analiza:** Testul `test_salary_third_bracket` a esuat, ceea ce demonstreaza ca suita de teste este indeajuns pentru a verifica comportamentul aplicatiei. 
* **Actiune:** Mutantul a fost omorat.