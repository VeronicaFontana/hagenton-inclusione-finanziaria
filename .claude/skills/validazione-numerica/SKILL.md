---
name: validazione-numerica
description: Come generare e strutturare test automatici che confrontano l'output del motore di calcolo del mutuo con casi di riferimento noti, incluse proprietà invarianti (somma quote capitale, monotonia interessi, TAEG>=TAN) e tolleranze di arrotondamento corrette. Usare quando si scrivono test per il motore di calcolo del mutuo o si valida un nuovo caso contro un simulatore reale.
---

# Validazione numerica

Dà credibilità al requisito "dati reali" della traccia: il motore di calcolo va testato contro casi noti, non solo contro se stesso. Le formule di riferimento sono in `formule-mutuo`; questa skill descrive **come testarle**.

## Struttura dei test

1. **Casi di riferimento fissi** (regression test): vedi [casi-test.md](casi-test.md). Ogni caso è `(capitale, TAN, durata, convenzione) → (rata attesa, interessi totali attesi)`.
2. **Test di proprietà** (property-based, validi per qualunque input valido, non solo i casi fissi):
   - la somma delle quote capitale del piano == capitale erogato (entro la tolleranza cumulata, vedi sotto)
   - la quota interessi è strettamente decrescente rata dopo rata (ammortamento francese)
   - la quota capitale è strettamente crescente rata dopo rata
   - il debito residuo dell'ultima rata è esattamente 0
   - `TAEG ≥ TAN` quando ci sono costi accessori positivi; `TAEG == TAN` (attuariale) solo a costi zero
   - la rata è sempre positiva e finita per capitale, tasso, durata validi (> 0)

## Tolleranza di arrotondamento — non usare una soglia fissa piccola

Ogni riga del piano arrotonda la propria quota capitale a 2 decimali (fino a 0,005 € di scarto per riga). Su un piano di `n` rate lo scarto cumulato sulla **somma** delle quote capitale arrotondate può crescere linearmente con `n`. Una tolleranza fissa come `0.01€` fallisce ingiustamente su piani lunghi (es. 240 rate).

Regola pratica: tolleranza cumulata = `numero_rate × 0.005€`. Il debito residuo finale, invece, deve essere sempre esattamente 0 (non è soggetto a questa tolleranza, perché l'ultima rata è costruita apposta per chiuderlo — vedi `piano_ammortamento()` in `formule-mutuo/reference.py`).

## Validare un nuovo caso contro un simulatore reale

Prima di aggiungere un caso a `casi-test.md` come fonte di verità:
1. Calcolare rata e piano con `formule-mutuo/reference.py`.
2. Inserire **gli stessi identici parametri** (capitale, TAN, durata, convenzione di conversione del tasso) in almeno un simulatore reale di un istituto di credito italiano.
3. Confrontare la rata risultante: uno scarto superiore a qualche centesimo/euro va investigato — può indicare una convenzione di conversione tasso diversa (lineare vs attuariale, vedi `formule-mutuo`), oppure costi/arrotondamenti specifici di quella banca.
4. Annotare in `casi-test.md` la fonte (nome banca/simulatore, data di verifica) accanto al caso, così il riferimento resta tracciabile e aggiornabile.

**Nota**: nessun caso in `casi-test.md` va considerato "verificato con dati reali" finché non ha superato questo confronto almeno una volta. I casi non ancora verificati vanno marcati esplicitamente come tali.

## Come scrivere i test (esempio di struttura, non vincolante sul framework)

```python
import pytest
from formule_mutuo.reference import rata_mensile, piano_ammortamento, tasso_mensile_da_annuo

@pytest.mark.parametrize("capitale,tan,anni,rata_attesa", [
    (100_000, 0.03, 20, 554.60),
    # ... altri casi da casi-test.md
])
def test_rata_contro_caso_noto(capitale, tan, anni, rata_attesa):
    i = tasso_mensile_da_annuo(tan, "lineare")
    rata = rata_mensile(capitale, i, anni * 12)
    assert rata == pytest.approx(rata_attesa, abs=0.01)

def test_somma_quote_capitale_uguale_capitale():
    capitale, i, n = 100_000, 0.0025, 240
    piano = piano_ammortamento(capitale, i, n)
    somma = sum(r.quota_capitale for r in piano)
    assert abs(somma - capitale) < n * 0.005

def test_debito_residuo_finale_zero():
    piano = piano_ammortamento(100_000, 0.0025, 240)
    assert piano[-1].debito_residuo == 0.0

def test_quota_interessi_decrescente():
    piano = piano_ammortamento(100_000, 0.0025, 240)
    interessi = [r.quota_interessi for r in piano]
    assert all(a >= b for a, b in zip(interessi, interessi[1:]))
```

Adattare framework/linguaggio a quello scelto per il motore di calcolo effettivo; la struttura dei casi e delle proprietà resta questa.
