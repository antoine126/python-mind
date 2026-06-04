"""Chapitre 3 — Types primitifs et (im)mutabilité : corrigés."""

from __future__ import annotations

from decimal import Decimal


# ---------------------------------------------------------------------------
# Exercice 1 — Refaire : prédire les effets
# ---------------------------------------------------------------------------
def modify(x: int, lst: list[int], text: str) -> None:
    x *= 2            # int immuable : recrée un objet local, n'affecte pas a
    lst.append(x)     # list mutable : modifie l'objet partagé
    text += "!"       # str immuable : nouvelle chaîne locale


def exercice_1() -> tuple[int, list[int], str]:
    a = 5
    b = [1]
    s = "hi"
    modify(a, b, s)
    # a reste 5, s reste "hi", b devient [1, 10] (x valait 10 à l'append)
    return a, b, s


# ---------------------------------------------------------------------------
# Exercice 2 — Comprendre : le total faux
# ---------------------------------------------------------------------------
def somme_correcte(qty: str, extra: str) -> int:
    """`"2" + "3"` concatène ("23") ; il faut convertir à la frontière."""
    return int(qty) + int(extra)


# ---------------------------------------------------------------------------
# Exercice 3 — Concevoir : un type pour des montants
# ---------------------------------------------------------------------------
def total_facture(lignes: list[str]) -> Decimal:
    """Additionne des montants en Decimal (exactitude base 10).

    On construit les Decimal depuis des CHAÎNES : `Decimal("9.99")`, pas
    `Decimal(9.99)` qui réintroduirait l'imprécision du float.
    """
    return sum((Decimal(montant) for montant in lignes), start=Decimal("0"))


def _checks() -> None:
    assert exercice_1() == (5, [1, 10], "hi")

    assert "2" + "3" == "23"  # le piège
    assert somme_correcte("2", "3") == 5

    # Le piège des flottants, et l'exactitude de Decimal.
    assert 0.1 + 0.2 != 0.3
    assert Decimal("0.1") + Decimal("0.2") == Decimal("0.3")
    assert total_facture(["9.99", "0.01", "5.00"]) == Decimal("15.00")


if __name__ == "__main__":
    _checks()
    print("chapitre 3 — corrigés OK")
