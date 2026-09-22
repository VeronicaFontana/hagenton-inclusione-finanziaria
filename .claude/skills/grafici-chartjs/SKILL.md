---
name: grafici-chartjs
description: Conoscenza codificata dell'API di Chart.js (chartjs.org) per creare o modificare grafici nel simulatore — setup via CDN, struttura config (type/data/options), contenitore responsive, aggiornamento dinamico di un grafico esistente (es. quando l'utente muove uno slider), grafici a barre impilate, e come farli coerenti con i colori e il tema chiaro/scuro del progetto. Usare ogni volta che si crea un nuovo grafico o si modifica uno esistente (mini-chart capitale/interessi, grafico inflazione, heatmap ottimizzatore, gauge punteggio salute), per evitare di reinventare un motore SVG a mano quando Chart.js è più adatto, o di inventare opzioni Chart.js plausibili ma inesistenti.
---

# Grafici con Chart.js

Questa skill è la fonte di verità per l'API di Chart.js in questo progetto. Il simulatore oggi disegna alcuni grafici "a mano" con `<svg>`/CSS generato in JS (barre capitale/interessi, curva inflazione, gauge punteggio salute, heatmap ottimizzatore). Quando si aggiunge un nuovo grafico o si riscrive uno esistente con Chart.js, usare esattamente i nomi di opzione e la struttura descritti qui — non improvvisare opzioni "che suonano plausibili".

Esempio funzionante completo, coerente con i colori e il tema del progetto: [reference-esempio.html](reference-esempio.html).

## 1. Setup: un solo `<script>` da CDN, niente build step

Il progetto è una singola pagina HTML senza bundler, quindi Chart.js va incluso via CDN, come già si fa per il font Inter:

```html
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
```

Va messo **prima** dello script principale della pagina (o comunque prima del primo `new Chart(...)`), altrimenti `Chart` non è ancora definito.

## 2. Struttura base di una config

Ogni grafico è un oggetto con tre chiavi, sempre queste tre:

```js
new Chart(ctx, {
  type: 'bar',       // 'line' | 'bar' | 'doughnut' | 'pie' | 'radar' | ...
  data: {
    labels: [...],           // etichette sull'asse (es. anni)
    datasets: [{
      label: 'Capitale',
      data: [...],            // stessa lunghezza di labels
      backgroundColor: '...',
      borderColor: '...',
    }]
  },
  options: { ... }
});
```

`ctx` è il **contesto 2D del canvas**, non il canvas stesso: `document.getElementById('mioChart').getContext('2d')`.

## 3. Contenitore responsive: obbligatorio, altrimenti il canvas cresce all'infinito

Chart.js ridimensiona il canvas osservando il suo **contenitore diretto**, non la finestra. Il contenitore deve essere `position: relative` e dedicato solo al canvas (nessun altro contenuto dentro):

```html
<div style="position: relative; height: 200px; width: 100%;">
  <canvas id="mioChart"></canvas>
</div>
```

Opzioni di default (di solito vanno bene così, non serve impostarle a mano):
- `responsive: true` — segue le dimensioni del contenitore
- `maintainAspectRatio: true` — mantiene il rapporto larghezza/altezza originale

**Errore comune da evitare**: impostare `width`/`height` in `%` o `vh` direttamente sull'attributo `<canvas width="...">` — non funziona (il canvas richiede numeri interi in pixel per quegli attributi). Se serve un'altezza fissa diversa dal rapporto di default, impostare `maintainAspectRatio: false` nelle `options` e dare un'altezza esplicita in px al contenitore.

## 4. Aggiornare un grafico esistente (slider, input numerici)

Il simulatore ha molti controlli live (slider durata, spread, importo...): **non distruggere e ricreare il grafico ad ogni cambiamento**, è lento e fa "lampeggiare" il canvas. Il pattern corretto è mutare `chart.data` e chiamare `chart.update()`:

```js
chart.data.labels = nuoveEtichette;
chart.data.datasets[0].data = nuoviValori;
chart.update();
```

Per aggiornamenti molto frequenti e continui (es. durante il drag di uno slider `input` in tempo reale, non solo al `change`), disabilitare l'animazione per evitare accumulo di frame:

```js
chart.update('none');
```

Tenere un riferimento all'istanza del grafico in una variabile di modulo (come si fa già con `state` per lo stato del simulatore), non ricrearla dentro la funzione di render principale.

## 5. Grafico a barre impilate (es. capitale vs interessi per anno)

Corrisponde al mini-chart già presente nel simulatore (barre `.bar.capitale` / `.bar.interessi`). Con Chart.js:

```js
new Chart(ctx, {
  type: 'bar',
  data: {
    labels: anni,
    datasets: [
      { label: 'Capitale', data: capitalePerAnno, backgroundColor: coloreBlu },
      { label: 'Interessi', data: interessiPerAnno, backgroundColor: coloreArancio },
    ]
  },
  options: {
    scales: {
      x: { stacked: true },
      y: { stacked: true, beginAtZero: true }
    }
  }
});
```

Impostare `stacked: true` su **entrambi** gli assi (x e y): dimenticarne uno lascia le barre affiancate invece che impilate — è l'errore più comune con questo tipo di grafico.

Altre proprietà utili sul dataset: `borderRadius` (arrotonda gli angoli delle barre, coerente con lo stile arrotondato del resto della UI) e `borderWidth`/`borderColor` per un contorno.

## 6. Colori coerenti col design system e col tema chiaro/scuro — punto critico

Il progetto definisce i colori come **custom property CSS** (`--blu`, `--verde`, `--arancio`, `--testo-soft`, ecc., vedi `:root` in `mutuo_educativo.html`) e li ricalcola per il tema scuro tramite `html[data-theme="dark"] { --blu-testo: ...; ... }`.

**Chart.js non capisce `var(--blu)` come colore.** Il canvas `<canvas>` è disegnato via API 2D (`fillStyle`, `strokeStyle`), che non fa parte della cascata CSS: passare la stringa letterale `'var(--blu)'` come `backgroundColor` non genera un errore, ma il colore risulta sbagliato/trasparente in modo silenzioso. Bisogna leggere il **valore calcolato** con `getComputedStyle` al momento della creazione/aggiornamento del grafico:

```js
function coloreCSS(nomeVar) {
  return getComputedStyle(document.documentElement).getPropertyValue(nomeVar).trim();
}
const blu = coloreCSS('--blu');
const arancio = coloreCSS('--arancio');
```

**Conseguenza per il toggle tema chiaro/scuro già presente nella pagina** (`toggleTema()`): cambiare `data-theme` su `<html>` aggiorna automaticamente tutti gli elementi DOM/CSS, ma **non** i canvas Chart.js già disegnati, perché i colori sono stati "congelati" come stringhe al momento della creazione. Se un grafico deve restare leggibile passando da tema chiaro a scuro, `toggleTema()` deve anche ricalcolare i colori dei dataset con `getComputedStyle` e chiamare `chart.update()` — vedi l'esempio in [reference-esempio.html](reference-esempio.html).

## 7. Accessibilità

Il `<canvas>` non ha contenuto testuale nativo per gli screen reader. Best practice minima:
- dare al canvas un `role="img"` e un `aria-label` descrittivo che riassuma il grafico in una frase (es. `aria-label="Composizione della rata: capitale e interessi per anno"`), aggiornato quando cambiano i dati;
- non affidarsi al solo colore per distinguere le serie (già garantito qui dalle etichette in `datasets[].label`, che Chart.js mostra nella legenda di default).

## 8. Quando NON usare Chart.js in questo progetto

Per micro-visualizzazioni molto semplici e statiche (una singola barra di progresso, il meter di sostenibilità, un arco di gauge) l'SVG/CSS fatto a mano resta preferibile: sono poche righe, zero dipendenze esterne, e non serve interattività/animazione della libreria. Chart.js conviene quando il grafico ha più serie di dati, assi, tooltip al passaggio del mouse, o deve aggiornarsi frequentemente in risposta a più input — è il caso del grafico capitale/interessi e del grafico inflazione, meno quello del gauge a singolo valore.
