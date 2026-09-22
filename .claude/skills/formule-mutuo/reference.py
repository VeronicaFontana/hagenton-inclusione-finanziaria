"""Funzioni di riferimento per il calcolo di un mutuo a rata costante (ammortamento francese).

Queste funzioni sono la fonte di verità numerica descritta in SKILL.md.
Il motore di calcolo del software puo' reimplementarle in un altro linguaggio,
ma deve produrre risultati numericamente equivalenti (vedi skill validazione-numerica).

Nessuna dipendenza esterna: solo libreria standard.
"""

from __future__ import annotations

from dataclasses import dataclass


def tasso_mensile_da_annuo(tan_annuo: float, convenzione: str = "lineare") -> float:
    """Converte un TAN annuo in tasso periodale mensile.

    convenzione:
      - "lineare": TAN / 12 (convenzione piu' diffusa nei fogli informativi bancari italiani)
      - "attuariale": (1 + TAN)^(1/12) - 1 (matematicamente corretta, composta)

    La convenzione usata DEVE essere esplicita nel codice chiamante e comunicata
    all'utente finale quando si spiega come e' stata calcolata la rata.
    """
    if convenzione == "lineare":
        return tan_annuo / 12
    if convenzione == "attuariale":
        return (1 + tan_annuo) ** (1 / 12) - 1
    raise ValueError(f"convenzione non riconosciuta: {convenzione!r}")


def rata_mensile(capitale: float, tasso_mensile: float, numero_rate: int) -> float:
    """Rata costante di un ammortamento francese.

    R = C * [ i * (1+i)^n ] / [ (1+i)^n - 1 ]
    """
    if numero_rate <= 0:
        raise ValueError("numero_rate deve essere positivo")
    if tasso_mensile == 0:
        return capitale / numero_rate
    fattore = (1 + tasso_mensile) ** numero_rate
    return capitale * (tasso_mensile * fattore) / (fattore - 1)


@dataclass(frozen=True)
class RigaPiano:
    numero_rata: int
    rata: float
    quota_interessi: float
    quota_capitale: float
    debito_residuo: float


def piano_ammortamento(
    capitale: float, tasso_mensile: float, numero_rate: int
) -> list[RigaPiano]:
    """Piano di ammortamento francese completo, rata per rata.

    Invarianti attese (vedi skill validazione-numerica):
      - somma delle quote capitale == capitale (a meno di arrotondamento sull'ultima rata)
      - quota_interessi strettamente decrescente, quota_capitale strettamente crescente
      - debito_residuo dell'ultima riga == 0
    """
    rata = rata_mensile(capitale, tasso_mensile, numero_rate)
    righe: list[RigaPiano] = []
    debito_residuo = capitale

    for numero in range(1, numero_rate + 1):
        interessi = debito_residuo * tasso_mensile
        capitale_quota = rata - interessi

        if numero == numero_rate:
            # L'ultima rata assorbe l'eventuale scarto di arrotondamento
            # cosi' che il debito residuo finale sia esattamente zero.
            capitale_quota = debito_residuo
            rata_finale = capitale_quota + interessi
        else:
            rata_finale = rata

        debito_residuo = debito_residuo - capitale_quota

        righe.append(
            RigaPiano(
                numero_rata=numero,
                rata=round(rata_finale, 2),
                quota_interessi=round(interessi, 2),
                quota_capitale=round(capitale_quota, 2),
                debito_residuo=round(max(debito_residuo, 0.0), 2),
            )
        )

    return righe


def taeg_da_flussi(
    capitale_netto_erogato: float,
    rata: float,
    numero_rate: int,
    costi_per_rata: list[float] | None = None,
    tolleranza: float = 1e-8,
    max_iterazioni: int = 200,
) -> float:
    """Calcola il TAEG annuo risolvendo l'equazione di equivalenza finanziaria:

        capitale_netto_erogato = sum_{k=1..n} (rata + costi_per_rata[k-1]) / (1+x)^(k/12)

    Trova x (tasso annuo) per bisezione. Il TAEG NON e' TAN + costante:
    va sempre risolto numericamente, vedi SKILL.md sezione 3.

    Solleva ValueError se il TAEG risultante e' inferiore al TAN implicito nella
    rata (indicherebbe un bug nel calcolo o nei flussi passati).
    """
    if costi_per_rata is None:
        costi_per_rata = [0.0] * numero_rate
    if len(costi_per_rata) != numero_rate:
        raise ValueError("costi_per_rata deve avere lunghezza numero_rate")

    flussi = [rata + costi_per_rata[k] for k in range(numero_rate)]

    def valore_attuale(tasso_annuo: float) -> float:
        return sum(
            flusso / (1 + tasso_annuo) ** ((k + 1) / 12)
            for k, flusso in enumerate(flussi)
        )

    basso, alto = 0.0, 1.0  # 0% - 100% annuo, range ampio a sufficienza per un mutuo
    for _ in range(max_iterazioni):
        medio = (basso + alto) / 2
        if valore_attuale(medio) > capitale_netto_erogato:
            basso = medio
        else:
            alto = medio
        if alto - basso < tolleranza:
            break

    taeg = (basso + alto) / 2

    if sum(costi_per_rata) > 0 and taeg < 0:
        raise ValueError("TAEG calcolato negativo con costi positivi: controllare i flussi")

    return taeg


if __name__ == "__main__":
    # Caso base di verifica citato in SKILL.md.
    capitale = 100_000.0
    tan_annuo = 0.03
    durata_anni = 20
    numero_rate = durata_anni * 12

    i_mensile = tasso_mensile_da_annuo(tan_annuo, convenzione="lineare")
    rata = rata_mensile(capitale, i_mensile, numero_rate)
    piano = piano_ammortamento(capitale, i_mensile, numero_rate)
    totale_interessi = sum(riga.quota_interessi for riga in piano)

    print(f"Rata mensile: {rata:.2f} EUR")
    print(f"Totale interessi: {totale_interessi:.2f} EUR")
    print(f"Debito residuo finale: {piano[-1].debito_residuo:.2f} EUR")

    # Tolleranza scalata sul numero di rate: ogni riga arrotonda la propria
    # quota_capitale a 2 decimali (fino a 0,005 EUR di scarto ciascuna), quindi
    # lo scarto cumulato sulla SOMMA delle righe arrotondate puo' crescere con n.
    # Il debito_residuo interno resta pero' esatto (non arrotondato durante il
    # calcolo), quindi l'ultima riga chiude sempre a zero: vedi assert sotto.
    somma_quote_capitale = sum(riga.quota_capitale for riga in piano)
    tolleranza_cumulata = numero_rate * 0.005
    assert (
        abs(somma_quote_capitale - capitale) < tolleranza_cumulata
    ), "somma quote capitale != capitale oltre la tolleranza attesa"
    assert piano[-1].debito_residuo == 0.0, "debito residuo finale non azzerato"
