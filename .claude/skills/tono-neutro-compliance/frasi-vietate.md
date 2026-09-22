# Frasi e pattern vietati

Lista di riferimento per il controllo automatico (regex/keyword) su ogni testo generato prima di mostrarlo all'utente. Non esaustiva: qualunque frase con lo stesso effetto comunicativo (raccomandare, classificare, giudicare un'opzione) va trattata come violazione anche se non è letteralmente in lista.

Il controllo deve essere case-insensitive e tollerante a coniugazioni/flessioni (es. "conviene", "converrebbe", "converrebbero").

## Consiglio esplicito
- ti conviene / vi conviene / conviene scegliere
- ti consiglio / consigliamo / raccomandiamo
- dovresti / dovreste (scegliere, optare, preferire)
- opta per / scegli / seleziona questo (in forma imperativa rivolta all'utente su un'opzione)
- la cosa giusta da fare è

## Classifica implicita
- la scelta migliore / la soluzione migliore
- l'opzione più conveniente / il mutuo più conveniente
- il mutuo ideale (per te / per la tua situazione)
- la soluzione ottimale
- decisamente meglio / nettamente preferibile

## Giudizio di valore mascherato da fatto
- è più sicuro (riferito a un'opzione senza specificare rispetto a cosa/quale rischio, in modo che implichi preferenza)
- è più intelligente / più furbo
- è la strada giusta

## Second person legato a una decisione
- "tu dovresti" / "lei dovrebbe" + verbo di scelta
- "se fossi in te" / "al tuo posto"
- "ti serve" (riferito a un prodotto specifico) quando implica raccomandazione, non un fatto neutro (es. "ti serve un documento X" è un fatto procedurale, ammesso; "ti serve questo tipo di mutuo" non lo è)

## Espressioni ammesse da non confondere con le precedenti

Queste NON sono violazioni, vanno distinte durante il controllo:
- descrizioni comparative fattuali ("la rata è più bassa", "gli interessi totali sono più alti") — ammesse se non seguite da un giudizio
- rimandi a un consulente/intermediario abilitato esterno al software
- avvisi procedurali neutri ("per procedere serve...", "è necessario presentare...")
