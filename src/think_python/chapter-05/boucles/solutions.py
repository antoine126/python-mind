"""Chapitre 5 — Boucles et itération : corrigés."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass


# ---------------------------------------------------------------------------
# Exercice 1 — Refaire : trois réécritures idiomatiques
# ---------------------------------------------------------------------------
def rewrite_a(names: list[str]) -> list[str]:
    return [name for name in names]            # itérer les éléments


def rewrite_b(values: list[int]) -> list[int]:
    return [x * 2 for x in values]             # compréhension


def rewrite_c(a: list[int], b: list[int]) -> list[tuple[int, int]]:
    return [(x, y) for x, y in zip(a, b)]      # zip, pas range(len(...))


# ---------------------------------------------------------------------------
# Exercice 2 — Comprendre : la suppression piégée
# ---------------------------------------------------------------------------
@dataclass
class Task:
    title: str
    is_done: bool = False
    is_late: bool = False


def remove_done(tasks: list[Task]) -> list[Task]:
    """On ne mute pas la liste itérée : on en construit une nouvelle."""
    return [t for t in tasks if not t.is_done]


# ---------------------------------------------------------------------------
# Exercice 3 — Concevoir : chercher le premier en retard
# ---------------------------------------------------------------------------
def first_late_loop(tasks: Iterable[Task]) -> Task | None:
    """for/else : explicite « cherché, rien trouvé »."""
    for task in tasks:
        if task.is_late:
            return task
    return None


def first_late_next(tasks: Iterable[Task]) -> Task | None:
    """next() + générateur + défaut : « le premier qui correspond, ou None »."""
    return next((t for t in tasks if t.is_late), None)


def _checks() -> None:
    assert rewrite_a(["a", "b"]) == ["a", "b"]
    assert rewrite_b([1, 2, 3]) == [2, 4, 6]
    assert rewrite_c([1, 2], [3, 4]) == [(1, 3), (2, 4)]

    tasks = [Task("a", is_done=True), Task("b"), Task("c", is_done=True)]
    assert remove_done(tasks) == [Task("b")]

    late = [Task("a"), Task("b", is_late=True), Task("c", is_late=True)]
    assert first_late_loop(late) == Task("b", is_late=True)
    assert first_late_next(late) == Task("b", is_late=True)
    assert first_late_loop([Task("a")]) is None
    assert first_late_next([Task("a")]) is None


if __name__ == "__main__":
    _checks()
    print("chapitre 5 — corrigés OK")
