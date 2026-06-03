"""Chapitre 1 — Le modèle mental de Python : corrigés des exercices.

Lancer : ``uv run python chapter-01/modele-mental/solutions.py``
"""

from __future__ import annotations

import copy


# ---------------------------------------------------------------------------
# Exercice 1 — Refaire : prédire la sortie
# ---------------------------------------------------------------------------
def exercice_1() -> tuple[list[int], list[int], bool, bool, bool]:
    """``b = a`` est un alias ; ``c = a.copy()`` est une copie indépendante."""
    a = [1, 2]
    b = a            # alias : même objet
    c = a.copy()     # copie : objet distinct, figé à [1, 2]
    b.append(3)      # mute la liste partagée par a et b
    # (1) a == [1, 2, 3]   a voit l'ajout via son alias b
    # (2) c == [1, 2]      copie indépendante
    # (3) a is b == True   même objet
    # (4) a == c -> False  valeurs différentes
    # (5) a is c == False  objets distincts
    return a, c, (a is b), (a == c), (a is c)


# ---------------------------------------------------------------------------
# Exercice 2 — Comprendre : le défaut piégé
# ---------------------------------------------------------------------------
def append_zero(values: list[int] | None = None) -> list[int]:
    """Renvoie une liste *neuve* à chaque appel (sentinelle ``None``).

    Le défaut ``[]`` aurait été créé une seule fois, à la définition de la
    fonction, et partagé entre tous les appels.
    """
    if values is None:
        values = []  # liste fraîche par appel
    values.append(0)
    return values


# ---------------------------------------------------------------------------
# Exercice 3 — Concevoir : un journal partagé… ou pas
# ---------------------------------------------------------------------------
# Deux signatures, deux choix d'ingénierie.

def record_event_shared(event: str, log: list[str]) -> None:
    """Journal *partagé* : l'appelant possède un unique objet mutable.

    Coût : couplage fort et aliasing voulu — une faute dans un module peut
    corrompre le journal de l'autre ; l'ordre devient sensible à la concurrence.
    """
    log.append(event)


def record_event_owned(event: str, log: list[str] | None = None) -> list[str]:
    """Journal *séparé* : chaque appelant repart d'un journal isolé.

    Coût : il faut *fusionner* les journaux pour une vue globale.
    """
    if log is None:
        log = []
    log.append(event)
    return log


def _checks() -> None:
    a, c, a_is_b, a_eq_c, a_is_c = exercice_1()
    assert a == [1, 2, 3]
    assert c == [1, 2]
    assert a_is_b is True
    assert a_eq_c is False
    assert a_is_c is False

    # Le bug est corrigé : deux appels, deux listes indépendantes.
    assert append_zero() == [0]
    assert append_zero() == [0]
    given = [1, 2]
    assert append_zero(given) == [1, 2, 0]

    # Journal partagé : une seule liste vue par deux « modules ».
    shared: list[str] = []
    record_event_shared("a", shared)
    record_event_shared("b", shared)
    assert shared == ["a", "b"]

    # Journaux séparés : isolation.
    assert record_event_owned("x") == ["x"]
    assert record_event_owned("y") == ["y"]

    # deepcopy : indépendance totale d'un graphe imbriqué.
    nested = [[1], [2]]
    clone = copy.deepcopy(nested)
    clone[0].append(99)
    assert nested == [[1], [2]]


if __name__ == "__main__":
    _checks()
    print("chapitre 1 — corrigés OK")
