---
name: glossario-linguaggio-semplice
description: Regole e definizioni di riferimento per spiegare in italiano semplice i termini di un mutuo (TAN, TAEG, spread, Euribor, piano di ammortamento, preammortamento, ecc.) senza perdere precisione tecnica. Usare ogni volta che si scrive testo esplicativo, tooltip, glossario o didascalie per l'utente finale del simulatore.
---

# Glossario e linguaggio semplice

Obiettivo: rendere comprensibili i termini finanziari a chi ha bassa alfabetizzazione finanziaria, **senza cambiarne il significato**. Una spiegazione semplificata che omette una condizione tecnica rilevante (es. "il TAEG è il tasso vero" senza dire che include i costi) non è una semplificazione: è un errore.

Per le formule esatte dietro questi termini, vedi la skill `formule-mutuo`. Questa skill riguarda solo *come comunicarle*.

## Regole di scrittura

1. **Una frase, un concetto.** Non incatenare più informazioni con "e" o subordinate multiple.
2. **Niente doppie negazioni.** Es. non "non è vero che non paghi interessi", ma "paghi comunque interessi".
3. **Ogni definizione astratta ha un esempio numerico concreto.** Non definire "spread" solo a parole: mostrare come si somma a un tasso di riferimento con numeri veri.
4. **Coerenza terminologica.** Lo stesso concetto si chiama sempre allo stesso modo in tutta l'app (mai "rata" in una schermata e "quota mensile" in un'altra per la stessa cosa).
5. **Niente metafore che distorcono.** Es. evitare "il TAEG è come lo scontrino finale, il TAN è il prezzo sullo scaffale" se questo implica che il TAN sia "falso" — va spiegato cosa include l'uno e cosa in più include l'altro, non giudicato.
6. **Definire prima di usare.** Un termine tecnico non va mai introdotto in UI senza che l'utente possa vederne la definizione (tooltip, sezione dedicata) nello stesso contesto.

## Termini chiave e definizione di riferimento

Ogni definizione qui sotto è la versione "lunga e corretta". Le versioni brevi in UI vanno derivate da queste senza perdere le condizioni indicate in *grassetto*.

- **TAN (Tasso Annuo Nominale)**: il tasso di interesse applicato al capitale prestato, su base annua. **Non include altri costi** del finanziamento.
- **TAEG (Tasso Annuo Effettivo Globale)**: il costo totale annuo del mutuo, **incluse le spese obbligatorie** per ottenerlo (istruttoria, incasso rata, assicurazione se obbligatoria). Serve a confrontare offerte diverse in modo omogeneo.
- **Spread**: il margine che la banca aggiunge a un tasso di riferimento di mercato (es. Euribor) per fissare il tasso applicato al cliente, nei mutui a tasso variabile o in fase di determinazione del tasso fisso.
- **Euribor**: tasso di interesse di riferimento del mercato interbancario europeo, usato come base per i mutui a tasso variabile. **Cambia nel tempo**, quindi la rata a tasso variabile può cambiare.
- **Tasso fisso**: il tasso di interesse resta identico per tutta la durata del mutuo; la rata **non cambia mai**, indipendentemente da come si muove il mercato.
- **Tasso variabile**: il tasso è ricalcolato periodicamente in base a un indice di mercato (es. Euribor) più lo spread; la rata **può aumentare o diminuire** nel tempo.
- **Piano di ammortamento**: la tabella che mostra, rata per rata, quanto si paga di interessi, quanto di capitale, e quanto resta da restituire.
- **Quota capitale / quota interessi**: in ogni rata, la parte che riduce il debito (quota capitale) e la parte che remunera la banca per il prestito (quota interessi). Nell'ammortamento francese la quota interessi è alta all'inizio e **diminuisce** nel tempo.
- **Preammortamento**: periodo iniziale in cui si pagano solo interessi, senza ridurre il capitale.
- **Imposta sostitutiva**: imposta dovuta allo Stato sull'erogazione del mutuo, in alternativa alle imposte ordinarie di registro/ipotecarie/catastali.
- **Spese di istruttoria**: costo una tantum che la banca applica per valutare ed erogare il mutuo.
- **LTV (Loan To Value)**: rapporto tra l'importo del mutuo richiesto e il valore dell'immobile. Un LTV più alto (es. 90%) di solito comporta condizioni meno favorevoli di un LTV più basso (es. 60%).
- **Garanzia ipotecaria**: diritto della banca di rivalersi sull'immobile se il mutuatario non paga.
- **Estinzione anticipata**: restituzione anticipata (totale o parziale) del debito residuo prima della scadenza naturale del mutuo.
- **Portabilità (surroga)**: possibilità di trasferire il mutuo residuo a un'altra banca, a condizioni diverse, senza costi di estinzione per il cliente.

## Checklist di verifica prima di pubblicare un testo semplificato

- [ ] Il testo semplificato mantiene tutte le condizioni tecniche della definizione di riferimento (nessuna omessa)?
- [ ] C'è un esempio numerico dove il termine è astratto?
- [ ] Il termine è usato in modo coerente con il resto dell'app?
- [ ] Nessuna doppia negazione, nessuna frase con più di un concetto?
- [ ] Il testo descrive, senza suggerire cosa "convenga" fare (vedi skill `tono-neutro-compliance`)?
