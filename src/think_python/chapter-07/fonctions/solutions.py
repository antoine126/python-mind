"""Chapitre 7 — Les fonctions : corrigés."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import date


# ---------------------------------------------------------------------------
# Exercice 1 — Refaire : nommer et purifier
# ---------------------------------------------------------------------------
@dataclass
class Task:
    title: str
    due: date
    cost: int


def sorted_by_due(tasks: list[Task]) -> list[Task]:
    """Pure : renvoie une nouvelle liste, ne mute pas l'argument."""
    return sorted(tasks, key=lambda t: t.due)


def total_cost(tasks: list[Task]) -> int:
    """Pure : un nombre en entrée, un nombre en sortie."""
    return sum(t.cost for t in tasks)


def report(tasks: list[Task]) -> None:
    """Le seul effet de bord — l'affichage — est isolé et nommé."""
    print(f"Total: {total_cost(tasks)}")


# ---------------------------------------------------------------------------
# Exercice 2 — Comprendre : la portée (LEGB)
# ---------------------------------------------------------------------------
def exercice_2() -> tuple[int, int]:
    n = 100

    def outer() -> int:
        n = 10                      # Enclosing pour inner

        def inner() -> int:
            return n + 1            # trouve n=10 dans la portée englobante

        return inner()

    return outer(), n               # (11, 100)


# ---------------------------------------------------------------------------
# Exercice 3 — Concevoir : une politique de tarification (Strategy)
# ---------------------------------------------------------------------------
@dataclass
class Usage:
    seats: int = 1


def free_price(usage: Usage) -> int:
    return 0


def pro_price(usage: Usage) -> int:
    return 9


def team_price(usage: Usage) -> int:
    return 5 * usage.seats


def monthly_bill(usage: Usage, price_fn: Callable[[Usage], int]) -> int:
    """price_fn est une fonction de première classe : ajouter un tarif =
    écrire une fonction, sans modifier monthly_bill."""
    return price_fn(usage)


def _checks() -> None:
    tasks = [
        Task("b", date(2026, 6, 2), 5),
        Task("a", date(2026, 6, 1), 3),
    ]
    assert [t.title for t in sorted_by_due(tasks)] == ["a", "b"]
    assert total_cost(tasks) == 8

    assert exercice_2() == (11, 100)

    assert monthly_bill(Usage(), free_price) == 0
    assert monthly_bill(Usage(), pro_price) == 9
    assert monthly_bill(Usage(seats=4), team_price) == 20


if __name__ == "__main__":
    _checks()
    print("chapitre 7 — corrigés OK")
