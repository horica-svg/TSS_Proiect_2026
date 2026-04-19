# CFG Mermaid - TaxEngine.calculate_annual_tax

```mermaid
flowchart TD
    A([Start calculate_annual_tax]) --> B{"Tipuri valide? (income numar, age int)"}
    B -- Nu / P1 --> E1([Return: Error Invalid Data Type])
    B -- Da / P2 --> C{Income in intervalul permis?}
    C -- Nu / P3 --> E2([Return: Error Invalid Income])
    C -- Da / P4 --> D{Age in intervalul permis?}
    D -- Nu / P5 --> E3([Return: Error Invalid Age])
    D -- Da / P6 --> E{Categorie valida?}
    E -- Nu / P7 --> E4([Return: Error Invalid Category])
    E -- Da / P8 --> F[Set tax = 0]

    F --> G{Categorie}
    G -- P9 --> S[salary: praguri 10k/50k]
    G -- P10 --> BZ[business: 25%; +5% >200k; -20% <20k]
    G -- P11 --> I[investment: 15%; +3% >100k; -15% <5k]
    G -- P12 --> FR[freelance: 12%; +8% >=50k rezident; -500 dependenti]
    G -- P13 --> CR[crypto: 10%; +20% >10k; x1.5 nerezident]
    G -- P14 --> RE[real_estate: praguri 50k/100k]
    S --> H
    BZ --> H
    I --> H
    FR --> H
    CR --> H
    RE --> H

    H{"Sectiunea 3: (age<25 si income<5000) sau (not resident si category!=crypto)?"}
    H -- Da / P15 --> H1[tax = tax * 0.9]
    H -- Nu / P16 --> H2{age>=65 si income<=30000?}
    H2 -- Da / P17 --> H3[tax = tax * 0.8]
    H2 -- Nu / P18 --> H4{age>=65 si income>30000?}
    H4 -- Da / P19 --> H5[tax = tax * 0.85]
    H4 -- Nu / P20 --> J
    H1 --> J
    H3 --> J
    H5 --> J

    J{"Sectiunea 4: married si dependenti si income<80000?"}
    J -- Da / P21 --> J1[tax = tax * 0.85]
    J -- Nu / P22 --> J2{married si fara dependenti?}
    J2 -- Da / P23 --> J3[tax = tax * 0.95]
    J2 -- Nu / P24 --> K
    J1 --> K
    J3 --> K

    K{tax < 0?}
    K -- Da / P25 --> K1[tax = 0]
    K -- Nu / P26 --> L["Return round(tax, 2)"]
    K1 --> L

    E1 -.->|error exit| A
    E2 -.->|error exit| A
    E3 -.->|error exit| A
    E4 -.->|error exit| A
    L -.->|final exit| A
```

## Notatii Pentru Independent Circuits

- P1-P8: validari si iesiri timpurii
- P9-P14: ramuri pe categorii fiscale
- P15-P20: ajustari sectiunea 3 (varsta, rezidenta, praguri)
- P21-P24: ajustari sectiunea 4 (stare civila si dependenti)
- P25-P26: tratament final (tax negativ vs return final)
- Muchiile punctate catre A sunt legaturi vizuale de tip dead-end, nu flux executabil normal
