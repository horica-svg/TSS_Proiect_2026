# Student 3 - Structural Coverage (White-Box)

👤 Student 3 (Structural Coverage - White-Box)

## Obiectiv
Atingerea unui procentaj de acoperire cat mai aproape de 100% si testarea structurilor logice complexe.

## Acoperire la nivel de Instructiune si Decizie
- Asigurarea ca testele trec prin liniile de deduceri specifice:
  - `tax -= 500` la categoria `freelance`.
  - `tax = tax * 1.5` la categoria `crypto` pentru non-rezidenti.
- Asigurarea ca se atinge linia `tax = 0` (evitarea taxelor negative):
  - exemplu: un freelancer cu venit foarte mic si dependenti care ar da un rezultat matematic negativ.

## Acoperire la nivel de Conditie (MC-DC)
Concentrare pe Sectiunea 3 si Sectiunea 4 din cod.

Pentru conditia:

`(age < 25 and income < 5000) or (not is_resident and category != "crypto")`

Trebuie scrise teste care demonstreaza ca fiecare operator influenteaza independent decizia finala (intrarea sau neintrarea pe ramura):
- `<`
- `and`
- `or`
- `not`
- `!=`

## Circuite Independente
- Calcularea Complexitatii Ciclomatice.
- Datorita numarului mare de `elif`, valoarea `V(G)` este ridicata (peste 15).
- Studentul 3 trebuie sa deseneze Graful de Control al Fluxului (CFG) pentru metoda de calcul a taxei.

## Implementare curenta in proiect
- Testele sunt organizate in stil structural coverage in fisierul `tests/test_tax_calculator.py` folosind `pytest`.
- Exista sectiuni dedicate pentru:
  - equivalence partitioning
  - boundary value analysis
  - category partitioning
  - statement coverage
  - branch coverage
  - condition coverage
  - circuits coverage
