# Raport Utilizare Tool AI (GitHub Copilot) în Testare

## 1. Introducere
În cadrul acestui proiect, am utilizat **GitHub Copilot** ca asistent pentru generarea de cod și teste unitare. Scopul a fost de a evalua eficiența tool-ului în identificarea cazurilor de testare relevante și în scrierea rapidă a suitei de teste.

## 2. Strategia de Utilizare
Am utilizat Copilot în două moduri principale:
1.  **Sugestii Inline:** Generarea automată a aserțiunilor pentru pragurile de impozitare bazate pe comentariile din cod.
2.  **Prompt-uri specifice:** Solicitarea generării unui set complet de teste pentru o anumită categorie (ex: "Generate pytest cases for the Crypto category including non-resident penalties").

## 3. Comparație: Teste Manuale vs. Teste Autogenerate

| Aspect | Teste Manuale | Teste Autogenerate (Copilot) |
| :--- | :--- | :--- |
| **Rapiditate** | Scăzuta (necesită calcul manual) | Foarte ridicată (sugestii instantanee) |
| **Acoperire Cazuri Marginale** | Bună (bazată pe analiză CFG) | Medie (tinde să repete cazuri similare) |
| **Precizie Calcule** | Ridicată (verificată manual) | Variabilă (uneori halucinează constantele) |
| **Structură** | Consistentă cu proiectul | Necesită ajustări pentru a respecta stilul |

### Exemplu Prompt și Răspuns
**Prompt:** `Create a test case for a married resident with 2 dependents and income of 60000 in the freelance category.`

**Răspuns Copilot:**
```python
def test_freelance_married_dependents():
    engine = TaxEngine()
    # Tax: 60000 * 0.12 = 7200
    # Dependents: 7200 - 500 = 6700
    # Married + Dependents + Income < 80k: 6700 * 0.85 = 5695
    assert engine.calculate_annual_tax(60000, "freelance", 30, True, True, True) == 5695.0
```

## 4. Analiza Diferențelor
Copilot a fost extrem de util pentru a genera "boiler-plate" code, dar a necesitat supraveghere atentă la calculele matematice complexe (cum ar fi ordinea aplicării reducerilor). În unele cazuri, Copilot a sugerat teste pentru ramuri care erau deja acoperite, fără a identifica drumurile independente (circuitele) cele mai dificile.

## 5. Capturi de Ecran
*(Aici s-ar include capturi de ecran cu sugestiile Copilot în IDE)*

## 6. Concluzii
GitHub Copilot este un instrument puternic care accelerează procesul de dezvoltare a testelor cu aproximativ 30-40%. Totuși, acesta nu poate înlocui analiza structurală riguroasă (CFG) și înțelegerea profundă a domeniului fiscal necesară pentru a garanta o acoperire de 100%.

## 7. Referințe Bibliografice
1. GitHub Copilot Documentation: https://docs.github.com/en/copilot
2. "AI-Assisted Software Testing": IEEE Software Magazine, 2024.
