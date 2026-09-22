# Casi di test di riferimento

Tutti i casi qui sotto sono calcolati con `formule-mutuo/reference.py`, convenzione di conversione tasso **lineare** (`TAN/12`), ammortamento francese, rate mensili.

**Stato attuale: nessun caso è ancora stato confrontato con un simulatore reale di banca.** Vanno usati per ora come test di regressione interni (garantiscono che il codice non cambi risultato silenziosamente), non come prova di correttezza contro "dati reali" — vedi procedura in SKILL.md per completare la verifica.

| Capitale | TAN annuo | Durata | Rate (n) | Rata mensile attesa | Interessi totali attesi | Verificato con simulatore reale? |
|---|---|---|---|---|---|---|
| 100.000 € | 3,00% | 20 anni | 240 | 554,60 € | 33.103,39 € | ❌ non ancora |
| 150.000 € | 2,50% | 25 anni | 300 | 672,93 € | 51.877,55 € | ❌ non ancora |
| 200.000 € | 4,00% | 30 anni | 360 | 954,83 € | 143.739,09 € | ❌ non ancora |
| 80.000 € | 3,50% | 15 anni | 180 | 571,91 € | 22.943,11 € | ❌ non ancora |
| 120.000 € | 2,00% | 10 anni | 120 | 1.104,16 € | 12.499,38 € | ❌ non ancora |

## Come aggiungere/aggiornare un caso

1. Calcolare con `formule-mutuo/reference.py` (vedi blocco `if __name__ == "__main__"` per un esempio d'uso, o importare le funzioni direttamente).
2. Inserire gli stessi parametri in un simulatore reale di un istituto di credito italiano.
3. Se lo scarto è entro pochi centesimi/euro, marcare la riga come verificata e annotare fonte + data:

```
| 100.000 € | 3,00% | 20 anni | 240 | 554,60 € | 33.103,39 € | ✅ verificato — Banca X, simulatore online, 2026-09-22 |
```

4. Se lo scarto è più ampio, indagare prima di aggiornare il valore atteso: controllare convenzione di conversione tasso (lineare vs attuariale), eventuali costi inclusi dal simulatore della banca, arrotondamenti specifici — vedi `formule-mutuo` SKILL.md sezione 2.
