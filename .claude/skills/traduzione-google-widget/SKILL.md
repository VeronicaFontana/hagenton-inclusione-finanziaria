---
name: traduzione-google-widget
description: Conoscenza codificata di come è integrato il selettore di lingua IT/EN/DE nel simulatore, basato sul widget Google Translate pilotato via JS (non un dizionario di traduzioni manuali). Copre perché è stata scelta questa strada invece di un i18n manuale, come si guida il widget dai pulsanti della UI senza mostrarne l'interfaccia di default, come si sopprime la banner-bar che Google inietta in cima alla pagina, e la natura asincrona dell'inizializzazione. Usare ogni volta che si modifica il selettore di lingua, si aggiunge una nuova lingua, o si tocca codice che interagisce con `google_translate_element` / `.goog-te-combo` in `mutuo_educativo.html`.
---

# Selettore di lingua: widget Google Translate

Il simulatore genera tutto il contenuto dinamicamente in italiano nel JS (centinaia di stringhe sparse in funzioni `renderXxx`). Tradurre a mano ogni stringa in EN/DE sarebbe un lavoro enorme da mantenere ad ogni modifica del testo. La scelta fatta per questo progetto è invece usare il motore di traduzione automatica di Google Translate, pilotato dai pulsanti IT/EN/DE nell'header, senza mostrare l'interfaccia standard del widget (che è pensata per apparire come banner in cima alla pagina).

**Compromesso accettato consapevolmente**: la qualità della traduzione sui termini tecnici finanziari (TAN, TAEG, spread...) non è garantita quanto un dizionario curato a mano — se in futuro serve precisione garantita su quei termini specifici, si può affiancare un dizionario manuale solo per il gergo tecnico chiave, senza sostituire l'approccio automatico per tutto il resto.

## 1. Come si pilota il widget senza la sua UI

Il widget standard di Google Translate si inizializza con:

```js
function googleTranslateElementInit() {
  new google.translate.TranslateElement({
    pageLanguage: 'it',
    includedLanguages: 'it,en,de',
    autoDisplay: false
  }, 'google_translate_element');
}
```

e lo script va caricato con `<script src="https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>`.

Questo crea un `<select>` nascosto (classe `.goog-te-combo`) dentro il div `#google_translate_element`. I pulsanti IT/EN/DE della UI **non** chiamano un'API di traduzione direttamente: impostano il `value` di quel `<select>` e disparano un evento `change`, che è ciò che fa scattare la traduzione della pagina:

```js
const combo = document.querySelector('.goog-te-combo');
combo.value = 'en';
combo.dispatchEvent(new Event('change'));
```

## 2. L'inizializzazione è asincrona: il `<select>` potrebbe non esistere ancora

Lo script di Google si carica e inizializza in modo asincrono. Se l'utente clicca un pulsante lingua prima che `.goog-te-combo` esista nel DOM, `document.querySelector` restituisce `null`. La funzione che gestisce il click deve quindi **ritentare con un piccolo delay** invece di fallire silenziosamente, con un numero massimo di tentativi per non ritentare all'infinito se lo script non si carica affatto (es. utente senza connessione):

```js
function setLanguage(lang, attempt = 0) {
  const combo = document.querySelector('.goog-te-combo');
  if (!combo) {
    if (attempt < 20) setTimeout(() => setLanguage(lang, attempt + 1), 250);
    return;
  }
  // ... imposta combo.value e dispatcha 'change'
}
```

## 3. Sopprimere la banner-bar che Google inietta in cima alla pagina

Il comportamento di default del widget è inserire una barra fissa in cima al documento ("Tradotto da Google Translate", pulsante "mostra originale") e spostare il contenuto della pagina verso il basso impostando uno stile inline su `<html>`/`<body>` (`top`/`margin-top`). In questo progetto quella barra va **sempre nascosta**, perché il selettore di lingua nell'header la sostituisce già.

Due livelli di difesa sono necessari, non uno solo:

1. **CSS**: nascondere gli elementi noti che Google inietta (`.goog-te-banner-frame`, `.goog-te-gadget-icon`, `.goog-te-menu-frame`, tooltip `.goog-tooltip`, ecc.) e forzare `top`/`margin-top` a `0` su `html`/`body`.
2. **JS con `MutationObserver`**: Google reimposta periodicamente lo stile inline `top`/`margin-top` su `<html>`/`<body>` per fare spazio alla barra — il solo CSS con `!important` non basta a impedirlo in ogni momento, quindi un `MutationObserver` che osserva i cambi di attributo `style` su `documentElement` e li azzera immediatamente è necessario per evitare che la barra compaia anche solo per un istante.

## 4. Non tradurre il selettore di lingua stesso

I pulsanti IT/EN/DE non devono essere tradotti dal widget (altrimenti "EN" potrebbe diventare "IT" quando si passa a tedesco, generando confusione). Il contenitore dei pulsanti va marcato con `class="notranslate"` e `translate="no"` — entrambi gli attributi sono rispettati da Google Translate e vanno tenuti insieme, non uno dei due soltanto.

## 5. Aggiungere una nuova lingua

Aggiungere una lingua richiede: un nuovo pulsante nella UI con `data-lang="<codice>"`, aggiungere `<codice>` alla stringa `includedLanguages` passata a `TranslateElement`, nessun'altra modifica — il resto del meccanismo (combo, MutationObserver, notranslate) è già generico.
