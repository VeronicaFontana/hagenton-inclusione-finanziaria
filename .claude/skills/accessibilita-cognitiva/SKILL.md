---
name: accessibilita-cognitiva
description: Checklist per revisionare la chiarezza generale di qualunque testo o label della UI del simulatore (non solo termini finanziari) pensata per utenti con bassa alfabetizzazione finanziaria — frasi brevi, un concetto per volta, terminologia coerente, divulgazione progressiva delle informazioni. Usare quando si scrive o revisiona testo di interfaccia (label, istruzioni, messaggi, riepiloghi) prima di mostrarlo all'utente.
---

# Accessibilità cognitiva

Questa skill riguarda la **chiarezza generale di ogni testo di interfaccia**, distinta da `glossario-linguaggio-semplice` (che riguarda specificamente la correttezza delle definizioni finanziarie) e da `tono-neutro-compliance` (che riguarda l'assenza di consigli). Un testo può essere corretto e neutro ma comunque difficile da capire per l'utente target — questa skill copre quel caso.

## Checklist di revisione per ogni testo/label

- [ ] **Frasi brevi.** Preferire frasi sotto le ~20 parole; spezzare frasi lunghe in più frasi brevi invece di usare subordinate multiple.
- [ ] **Un concetto per volta.** Ogni frase comunica una sola informazione nuova; non accorpare definizione + esempio + eccezione nella stessa frase.
- [ ] **Niente doppie negazioni.** Riformulare in positivo quando possibile.
- [ ] **Terminologia coerente.** Lo stesso concetto ha sempre la stessa etichetta in tutta l'app (coordinarsi con `glossario-linguaggio-semplice` per i termini finanziari, ma la regola vale anche per label generiche di UI: es. non chiamare lo stesso pulsante "Calcola" in una schermata e "Simula" in un'altra).
- [ ] **Niente sovraccarico numerico.** Non mostrare più di 4-5 numeri/valori diversi nella stessa schermata senza raggruppamento visivo o gerarchia; se servono più dati, suddividerli in sezioni.
- [ ] **Divulgazione progressiva.** Mostrare prima l'informazione essenziale (es. importo della rata), poi permettere di approfondire (es. piano di ammortamento completo, dettaglio costi) solo su richiesta esplicita dell'utente — non tutto insieme di default.
- [ ] **Gerarchia visiva del testo.** Usare liste puntate/numerate invece di paragrafi lunghi quando si elencano più elementi (costi, termini, passaggi); usare intestazioni per separare sezioni logiche.
- [ ] **Esempi concreti invece di astrazioni.** Preferire "su una rata di 500€, circa 200€ vanno a interessi e 300€ riducono il debito" a spiegazioni puramente concettuali.
- [ ] **Etichette dei campi di input chiare e senza gergo non spiegato.** Un campo che chiede il TAN deve avere un'etichetta comprensibile anche a chi non conosce il termine (con eventuale tooltip di rimando al glossario), non solo la sigla.

## Quando usare questa skill vs le altre

- Sto scrivendo la *definizione* di un termine finanziario (es. cos'è lo spread)? → `glossario-linguaggio-semplice`.
- Sto scrivendo un testo che *confronta scenari* o riassume risultati? → applicare prima `tono-neutro-compliance` (per il contenuto), poi questa skill (per la forma).
- Sto scrivendo *qualunque altra label, istruzione o messaggio di UI*? → questa skill.

Le tre skill vanno spesso applicate in sequenza sullo stesso testo, non in alternativa.
