class: center, middle

# Analiza și Testarea Aplicației Tax Calculator
## Proiect TSS 2026
### Stefan Tacu

---

# 1. Introducere și Configurație

- **Obiectiv:** Testarea riguroasă a unei aplicații de calcul fiscal.
- **Stack Tehnic:**
  - Python 3.13.2, Pytest 8.1.1
  - Radon (Complexity), Mutmut (Mutation)
  - Coverage.py (Structural Coverage)
- **Funcționalitate:** Calcul taxe pe categorii (Salary, Business, Crypto, etc.) cu aplicare de deduceri complexe.

---

# 2. Testare Funcțională (Black-Box)

- **Tehnici:** Equivalence Partitioning & Boundary Value Analysis.
- **Clase de Echivalență:**
  - Venit: Valid [0, 1M], Invalid (<0, >1M).
  - Vârstă: Valid [0, 150], Invalid.
  - Categorii: 6 categorii valide + ramură default.
- **Status:** 100% teste funcționale trecute.

---

# 3. Analiza Structurală: Teoria McCabe

- **Complexitate Ciclomatică (CC):** Măsură a numărului de circuite liniar independente.
- **Formula McCabe:** $V(G) = e - n + 2p$ (unde $p=1$ pentru o subrutină).
- **Aplicație:** În proiectul nostru, $V(G) = 41$ (Grad F).
- **Testarea Circuitelor Independente:**
  - Identifică limita superioară pentru numărul de căi necesare acoperirii ramurilor.
  - **Set de bază:** Orice cale prin program se poate forma ca o combinație din acest set.
- **Avantaj:** Setul poate fi generat pentru a garanta *Branch Coverage* 100%.

---

# 4. Rezultate Acoperire Structurală

<center>
    <img src="capturi_ecran/statement_coverage/branch-coverage-branch.png" width="85%">
</center>

- **Statement Coverage:** 100%
- **Branch Coverage:** 100% (obținut după rafinarea suitei de teste pentru a acoperi ramurile `else` implicite).

---

# 5. Testarea prin Mutație (Mutation Testing)

- **Instrument:** `mutmut` (mutanți de ordin 1).
- **Rezultate Automate:**
  - Total mutanți: 228
  - Omorâți: 181
  - **Mutation Score: 79.3%**
- **Analiză Manuală:** Scor de 72.7% pe un eșantion reprezentativ de 22 de mutanți.

---

# 6. Analiza Mutanților: Supraviețuitori

- **Mutanți Echivalenți:** Modificarea `>` în `>=` la praguri unde diferența este zero (ex: Business category).
- **Lipsă Precizie:** Supraviețuirea la modificarea rotunjirii (`round(tax, 1)`) a indicat aserțiuni prea permisive.
- **Îmbunătățire:** Rezultatele au condus la adăugarea de teste de frontieră mai stricte pentru categoriile Investment și Freelance.

---

# 7. Utilizare AI: GitHub Copilot

- **Eficiență:** Creștere cu ~40% a vitezei de scriere a testelor de tip boiler-plate.
- **Puncte Forte:** Sugestii rapide pentru clasele de echivalență standard.
- **Puncte Slabe:** Riscul de "halucinații" la calcule matematice complexe și omiterea cazurilor de frontieră pe logica de CC 41.
- **Concluzie:** AI-ul este un copilot, dar decizia de testare rămâne la inginer.

---

# 8. Concluzii

- **Rigoare:** Branch Coverage de 100% este necesar dar nu suficient fără Mutation Testing.
- **Complexitate:** Codul cu CC 41 (Rank F) este greu de întreținut și necesită teste automate dense.
- **Validare:** Integrarea metodelor manuale cu cele automate oferă cel mai înalt grad de încredere în software.

---

class: center, middle

# Vă mulțumesc!
## Întrebări și discuții.
