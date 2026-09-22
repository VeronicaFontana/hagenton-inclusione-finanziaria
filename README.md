# Capire il mutuo - hagenton
Creare un software che permetta all'utente con bassa alfabetizzazione finanziaria di simulare le rate del mutuo in base a dei parametri che inserisce, con educazione sui termini utilizzati e i risultati.

## Avvio in locale

L'app è una singola pagina HTML statica (`app/mutuo_educativo.html`), senza build step. Per aprirla nel browser:

```bash
npm install
npm start
```

Il comando avvia un server locale su `http://localhost:8080/mutuo_educativo.html` e apre automaticamente il browser. Le modifiche al file HTML sono visibili ricaricando la pagina (nessuna cache, nessuna compilazione necessaria).

## Presentazione

`capire_il_mutuo.html` è una presentazione statica che introduce il progetto. Per avviarla:

```bash
npm run presentazione
```

Il comando serve l'intera cartella del progetto su `http://localhost:8090/capire_il_mutuo.html` e apre automaticamente il browser. L'ultima slide contiene il pulsante "Inizia a esplorare →", che rimanda direttamente a `app/mutuo_educativo.html` sullo stesso server: non serve avviare `npm start` in parallelo per seguire questo percorso.

