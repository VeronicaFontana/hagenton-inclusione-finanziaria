---
name: tono-neutro-compliance
description: Verifica che qualunque testo o logica di confronto tra scenari generata per l'utente sia neutra e non contenga consigli o raccomandazioni finanziarie. Usare come revisione obbligatoria prima di mostrare o mergiare testi esplicativi, riepiloghi, confronti tra scenari di mutuo (fisso vs variabile, durate diverse, ecc.) generati per l'utente finale.
---

# Tono neutro / compliance

Vincolo centrale di questo progetto: **il software non è un consulente finanziario**. Non deve mai dire all'utente cosa scegliere, nemmeno implicitamente. Questo vale per ogni testo generato: spiegazioni, riepiloghi, confronti tra scenari (es. tasso fisso vs variabile, 20 anni vs 30 anni).

Questa skill va applicata come **revisione obbligatoria** prima di mostrare o mergiare qualunque testo generato dinamicamente o qualunque logica che confronti più scenari.

## Cosa è vietato

Frasi o pattern che esprimono una raccomandazione, un giudizio di valore, o una classifica implicita tra opzioni. Lista non esaustiva in [frasi-vietate.md](frasi-vietate.md) — usarla come base per un controllo automatico (regex/keyword scan) sul testo generato prima di mostrarlo.

Categorie di violazione:
- **Consiglio esplicito**: "ti conviene", "ti consiglio", "dovresti scegliere", "scegli X".
- **Classifica implicita**: "la scelta migliore", "l'opzione più conveniente", "il mutuo ideale per te".
- **Giudizio di valore mascherato da fatto**: "un tasso fisso è più sicuro" (affermazione presentata come oggettiva ma che implica una preferenza) invece di "con tasso fisso la rata non cambia nel tempo" (fatto verificabile, senza giudizio).
- **Second person prescrittivo legato a un'azione finanziaria**: qualunque frase in cui il soggetto "tu/lei" è collegato a un verbo di scelta/decisione riguardo al prodotto finanziario.

## Cosa è permesso (framing neutro)

- Presentare scenari fianco a fianco con numeri, senza etichettarli.
- Descrivere un trade-off come fatto reciproco, senza concludere quale lato "vince":
  - ✅ "Con tasso fisso la rata resta invariata per tutta la durata. Con tasso variabile la rata può aumentare o diminuire in base all'andamento dell'Euribor."
  - ❌ "Il tasso fisso è più sicuro, quindi se vuoi stare tranquillo scegli questo."
- Mostrare conseguenze quantitative senza qualificarle come buone o cattive: "Con una durata di 30 anni la rata mensile è più bassa, ma il totale degli interessi pagati nel tempo è più alto."
- Rimandare esplicitamente a un consulente/intermediario abilitato per qualunque decisione: è l'unica forma di indicazione "verso un'azione" ammessa, perché delega la decisione fuori dal software.

## Procedura di review

Da eseguire su ogni testo generato dinamicamente (spiegazioni, riepiloghi, output di confronto scenari) prima che venga mostrato all'utente o mergiato nel codice:

1. Scansionare il testo contro i pattern in `frasi-vietate.md`.
2. Per ogni frase che confronta due o più scenari, verificare che nessuno dei due sia presentato come preferibile (né esplicitamente né con aggettivi/avverbi che impliegano preferenza: "meglio", "ideale", "consigliato", "ottimale").
3. Se un pattern vietato viene rilevato, riscrivere la frase in forma di fatto verificabile (numero, condizione), non di giudizio — vedi esempi sopra.
4. In caso di dubbio su una frase borderline, preferire sempre la versione più neutra tra le alternative possibili.

## Nota su dati e non su opinioni

Questa skill riguarda il *testo generato* (linguaggio naturale). Il motore di calcolo può e deve produrre numeri comparativi (rata, interessi totali, ecc.) — non è questo ad essere vietato. È vietato **etichettare** quei numeri con un giudizio.
