# Testare Functionala - Tax Calculator



Pentru testarea functionala (Black-Box) a modulului `TaxEngine`, am folosit tehnicile **Partitionarea in Clase de Echivalenta (ECP)** si **Analiza Valorilor de Frontiera (BVA)**. Scopul a fost sa verificam corectitudinea calculului de taxe pe baza cerintelor si pragurilor de impozitare, tratand functia ca pe o "cutie neagra".



## 1. Analiza Datelor de Intrare (Validari la limita)

Am testat limitele absolute ale sistemului pentru a verifica robustetea la date incorecte:

* **Venit (Income):** Intervalul valid definit este `[0, 1000000]`. Am testat exact valorile de frontiera invalide din afara intervalului: `-1` si `1000001`.

* **Varsta (Age):** Intervalul valid este `[0, 150]`. Am testat valorile de frontiera invalide `-1` si `151`.

* **Categorii:** Am testat comportamentul sistemului la introducerea unei categorii de venit care nu face parte din setul acceptat.



## 2. Aplicarea ECP si BVA pe Categoriile de Venit



### Categoria "Salary" (Exemplu detaliat)

Am identificat urmatoarele clase de echivalenta si am aplicat analiza valorilor de frontiera pe baza pragurilor:

* **Clasa 1 (Venit <= 10000):** Se aplica o taxa de 10%.

    * *Valoare testata (BVA):* `10000` (limita superioara exacta a clasei).

    * *Valoare testata (ECP):* `5000` (valoare nominala, reprezentativa pentru interiorul clasei).

* **Clasa 2 (Venit 10001 - 50000):** Taxa de baza fixa + 15% pentru suma ce depaseste 10000.

    * *Valoare testata (ECP):* `30000`.

    * *Valoare testata (BVA):* `50000` (limita superioara).

* **Clasa 3 (Venit > 50000):** Taxa de baza fixa + 20% pentru suma ce depaseste 50000.

    * *Valoare testata (ECP):* `100000`.



### Celelalte Categorii (Business, Investment, Freelance, Crypto, Real Estate)

S-au creat teste similare selectand cate o valoare nominala (ECP) pentru situatiile standard si valori specifice pentru a declansa ramurile de suprataxare sau reducere. De exemplu:

* Pragul de `200000` pentru suprataxarea afacerilor.

* Pragul de `5000` pentru deducerea investitiilor mici.



## 3. Testarea Regulilor Compuse (Decision Table Logic)

Am adaugat scenarii specifice pentru a acoperi combinarea mai multor reguli de business (deduceri si penalizari):

* **Tineri cu venit mic:** Am verificat aplicarea reducerii de 10% pentru `varsta < 25` SI `venit < 5000`.

* **Seniori:** Am verificat pragurile de deducere pentru persoanele `>= 65 de ani`, atat pentru venituri sub `30000` (reducere 20%), cat si peste (reducere 15%).

* **Situatia familiala:** Am testat aplicarea deducerii compuse (15%) pentru clientii casatoriti cu dependenti si cu venit limitat.

* **Penalizari Crypto:** Am validat aplicarea factorului de multiplicare `x1.5` pentru utilizatorii non-rezidenti.







![Rezultate Testare Functionala](capturi_ecran/functional_testing/teste-trecute.png)



## Concluzii

Analiza functionala a demonstrat ca aplicatia respecta cu strictete regulile de business impuse. Utilizarea tehnicilor ECP si BVA ne-a asigurat ca am acoperit atat cazurile de utilizare frecvente (valori nominale), cat si situatiile limita sau datele invalide. Toate cele 21 scenarii de test implementate au trecut cu succes, confirmand ca `TaxEngine` calculeaza corect taxele, deducerile si penalizarile, oferind o baza solida inainte de a trece la testarea structurala.

