---
name: formule-mutuo
description: Conoscenza codificata delle formule corrette per simulare un mutuo — ammortamento francese, conversione tasso annuo/periodale, calcolo TAN→TAEG, preammortamento, estinzione anticipata. Usare ogni volta che si scrive o modifica codice di calcolo per rate, piani di ammortamento, TAN, TAEG, spread, Euribor, tasso fisso o variabile, per evitare di reinventare formule plausibili ma sbagliate.
---

# Formule mutuo

Questa skill è la fonte di verità per qualunque calcolo relativo a un mutuo in questo progetto. Se il codice di calcolo diverge da queste formule, è il codice ad essere sbagliato, non la skill: prima di "aggiustare" un test che fallisce, verificare qui la formula corretta.

Le funzioni di riferimento eseguibili sono in [reference.py](reference.py). Il motore di calcolo del software può reimplementarle (es. in un altro linguaggio), ma deve produrre risultati numericamente equivalenti — vedi la skill `validazione-numerica` per i test di confronto.

## 1. Ammortamento francese (rata costante)

È lo schema standard per i mutui a tasso fisso in Italia: la rata resta identica per tutta la durata, ma la composizione cambia — all'inizio prevalgono gli interessi, verso la fine prevale il rimborso di capitale.

Formula della rata periodale:

```
R = C × [ i × (1+i)^n ] / [ (1+i)^n − 1 ]
```

dove:
- `C` = capitale erogato (importo del mutuo)
- `i` = tasso di interesse **periodale** (es. mensile, non annuo — vedi sezione 2)
- `n` = numero totale di rate (es. anni × 12 per rate mensili)

Ad ogni rata `k` (da 1 a n):
- `interessi_k = debito_residuo_(k-1) × i`
- `capitale_k = R − interessi_k`
- `debito_residuo_k = debito_residuo_(k-1) − capitale_k`

Proprietà che devono sempre valere (vedi anche `validazione-numerica`):
- la somma di tutte le `capitale_k` è uguale a `C` (a meno di arrotondamenti sull'ultima rata)
- `interessi_k` è strettamente decrescente nel tempo, `capitale_k` è strettamente crescente
- `debito_residuo_n = 0`

## 2. Conversione tasso annuo → periodale: attenzione, esistono due convenzioni

Questo è un punto in cui è facile introdurre un errore silenzioso, perché entrambe le convenzioni sono "plausibili" e producono numeri vicini ma diversi.

**Convenzione attuariale (composta), matematicamente corretta:**
```
i_mensile = (1 + TAN)^(1/12) − 1
```

**Convenzione lineare (semplice), usata da molte banche italiane nei fogli informativi:**
```
i_mensile = TAN / 12
```

Le due convenzioni danno rate leggermente diverse (differenza tipicamente di pochi euro al mese su un mutuo standard). **Il codice deve rendere esplicita e configurabile quale convenzione sta usando**, mai darla per scontata implicitamente, e la UI deve poter dichiarare all'utente quale delle due sta applicando quando mostra "come è stata calcolata la rata". Di default, se non diversamente specificato dai dati reali della banca simulata, usare la convenzione lineare (`TAN/12`) perché è quella più diffusa nei fogli informativi europei standardizzati (SECCI/PIES).

## 3. TAN vs TAEG — non sono la stessa cosa "con una percentuale in più"

- **TAN** (Tasso Annuo Nominale): tasso di interesse puro applicato al capitale. Non include alcun costo accessorio.
- **TAEG** (Tasso Annuo Effettivo Globale): rappresenta il costo totale reale del credito su base annua, e include TAN + tutti i costi obbligatori per ottenere il finanziamento (spese di istruttoria, spese di incasso rata, assicurazione obbligatoria se richiesta come condizione per erogare il mutuo, imposta sostitutiva se applicabile). **Non include** costi facoltativi (es. assicurazioni non obbligatorie) né spese notarili non legate all'erogazione del credito.

Il TAEG **non si calcola con una formula chiusa additiva** (non è "TAN + 0.3%"): si calcola risolvendo l'equazione di equivalenza finanziaria che eguaglia il capitale netto erogato alla somma attualizzata di tutte le rate e i costi, cioè trovando il tasso `x` che soddisfa:

```
C_netto = Σ_{k=1..n} (R + costo_k) / (1 + x)^(k/12)
```

Questo equivale a un calcolo di tipo IRR (tasso interno di rendimento) e va risolto numericamente (es. Newton-Raphson o bisezione), non analiticamente. Vedi `taeg_da_flussi()` in reference.py.

**Regola di dominio da rispettare sempre:** `TAEG ≥ TAN` (se ci sono costi aggiuntivi; sono uguali solo nel caso limite di zero costi accessori). Se un calcolo produce TAEG < TAN, è un bug.

## 4. Preammortamento

Periodo iniziale (tipicamente tra l'erogazione e la prima rata "piena") in cui il mutuatario paga solo interessi sul capitale erogato, senza rimborso di quota capitale. Il piano di ammortamento vero e proprio (con quota capitale) inizia solo dopo. Se il software simula il preammortamento, deve trattarlo come una fase separata dal piano principale, non "spalmarla" dentro il calcolo della rata costante.

## 5. Estinzione anticipata

Rimborso, totale o parziale, del debito residuo prima della scadenza naturale. Effetti da modellare correttamente se implementato:
- il debito residuo ad una data rata `k` è quello calcolato al punto 1 (`debito_residuo_k`), non una proporzione lineare del capitale iniziale
- l'estinzione anticipata riduce gli interessi futuri (che si calcolano sul debito residuo), ma **non restituisce** interessi già pagati
- eventuali penali di estinzione anticipata (quando previste contrattualmente) sono un costo separato, non vanno confuse con gli interessi

## Esempi numerici di verifica

Caso base per test di regressione (usa convenzione lineare `TAN/12`):

```
Capitale (C):      100.000 €
TAN annuo:          3,00 %
Durata:             20 anni (n = 240 rate mensili)
i_mensile:          3,00% / 12 = 0,25% = 0,0025

Rata attesa (R):     ≈ 554,60 €
Totale interessi:    ≈ 33.103 €  (554,60 × 240 − 100.000)
```

Questi valori sono generati con `reference.py` — vedi `validazione-numerica` per come vanno confermati anche contro un simulatore reale di banca prima di essere usati come riferimento definitivo nei test.
