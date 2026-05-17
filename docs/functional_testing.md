# Analiza Testarii Functionale (Functional Testing Analysis)

Testarea functionala s-a concentrat pe verificarea cerintelor aplicatiei `Tax_Calculator` fara a lua in considerare structura interna a codului. Am utilizat tehnici precum **Analiza Valorilor de Frontiera (Boundary Value Analysis)** si **Partitionarea pe Clase de Echivalenta (Equivalence Partitioning)**.

## 1. Clase de Echivalenta si Valori de Frontiera

### Validari de intrare
Am identificat urmatoarele clase pentru datele de intrare:
- **Income (Venit):**
    - Valide: `[0, 1000000]`
    - Invalide: `< 0`, `> 1000000`, Tipuri non-numerice.
- **Age (Varsta):**
    - Valide: `[0, 150]`
    - Invalide: `< 0`, `> 150`, Tipuri non-numerice.
- **Category (Categorie):**
    - Valide: `salary`, `business`, `investment`, `freelance`, `crypto`, `real_estate` (si orice alt string valid).
    - Invalide: Categorii care nu sunt permise de aplicatie (desi codul trateaza orice categorie necunoscuta in ramura `else`).

### Praguri de impozitare (Exemplu: Salary)
- **Bracket 1:** `<= 10000` (Taxa 10%)
- **Bracket 2:** `(10000, 50000]` (Taxa fixa + 15% din ce depaseste 10000)
- **Bracket 3:** `> 50000` (Taxa fixa + 20% din ce depaseste 50000)

## 2. Cazuri de Testare Implementate

Suita de teste functionale se afla in `tests/functional-testing/test_functional_tax_calculator.py` si include:

| ID Test | Descriere | Input | Rezultat Asteptat |
| :--- | :--- | :--- | :--- |
| `test_invalid_data_types` | Tipuri de date incorecte | `income="1000"`, `age="30"` | `"Error: Invalid Data Type"` |
| `test_invalid_income_boundaries` | Venit in afara limitelor | `income=-1`, `income=1000001` | `"Error: Invalid Income"` |
| `test_invalid_age_boundaries` | Varsta in afara limitelor | `age=-1`, `age=151` | `"Error: Invalid Age"` |
| `test_salary_first_bracket` | Salariu prag 1 | `income=5000`, `income=10000` | `500.0`, `1000.0` |
| `test_discount_senior_low_income` | Reducere Senior (Varsta 65) | `age=65`, `income=20000` | `2000.0` (20% reducere) |
| `test_business_brackets` | Business - venit mare | `income=300000` | `80000.0` |

## 3. Rezultatele Rularii Testelor

Rularea testelor functionale a confirmat ca aplicatia respecta specificatiile pentru cazurile nominale si pentru gestionarea erorilor de baza.

![Teste Functionale Trecute](capturi_ecran/functional_testing/teste-trecute.png)

## 4. Concluzii
Suita de teste functionale ofera o baza solida pentru validarea corectitudinii calculelor fiscale. Desi acopera majoritatea scenariilor de business, analiza ulterioara a acoperirii structurale si a mutantilor a evidentiat necesitatea unor teste suplimentare pentru ramuri logice complexe si cazuri marginale.
