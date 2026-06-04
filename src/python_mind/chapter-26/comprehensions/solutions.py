"""Chapitre 26 — Compréhensions et style fonctionnel : corrigés."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass


@dataclass
class Task:
    id: int
    title: str
    done: bool = False
    cost: int = 0
    tags: tuple[str, ...] = ()


# ---------------------------------------------------------------------------
# Exercice 1 — Refaire : boucle vers compréhension (dict)
# ---------------------------------------------------------------------------
def done_titles_by_id(tasks: list[Task]) -> dict[int, str]:
    return {task.id: task.title for task in tasks if task.done}


# ---------------------------------------------------------------------------
# Exercice 2 — Comprendre : trop dense -> boucle nommée
# ---------------------------------------------------------------------------
def select(grid: list[list[int]], g: Callable[[int], int]) -> list[int]:
    """La compréhension d'origine appelait g(x) DEUX fois par élément retenu.

    En boucle nommée, on calcule g(x) une seule fois — lisible ET efficace.
    """
    out: list[int] = []
    for row in grid:
        for x in row:
            if x and x % 2 == 0:
                value = g(x)            # calculé une fois
                if value > 10:
                    out.append(value)
    return out


# ---------------------------------------------------------------------------
# Exercice 3 — Concevoir : choisir la forme
# ---------------------------------------------------------------------------
def total_cost(tasks: list[Task]) -> int:
    """(a) Réduction : expression génératrice (pas de liste intermédiaire)."""
    return sum(t.cost for t in tasks)


def done_map(tasks: list[Task]) -> dict[int, str]:
    """(b) Construction lisible : compréhension de dict."""
    return {t.id: t.title for t in tasks if t.done}


def notify_all(tasks: list[Task], send: Callable[[Task], None]) -> None:
    """(c) Action (effet de bord) : une boucle, pas une compréhension."""
    for t in tasks:
        send(t)


def unique_tags_sorted(tasks: list[Task]) -> list[str]:
    """(d) Compréhension de set (dédup) puis tri."""
    return sorted({tag for t in tasks for tag in t.tags})


def _checks() -> None:
    tasks = [
        Task(1, "a", done=True, cost=5, tags=("x", "y")),
        Task(2, "b", cost=3, tags=("y", "z")),
    ]
    assert done_titles_by_id(tasks) == {1: "a"}

    grid = [[2, 7, 8], [0, 12, 5]]
    assert select(grid, g=lambda x: x * 2) == [16, 24]   # 8*2=16, 12*2=24

    assert total_cost(tasks) == 8
    assert done_map(tasks) == {1: "a"}
    seen: list[int] = []
    notify_all(tasks, lambda t: seen.append(t.id))
    assert seen == [1, 2]
    assert unique_tags_sorted(tasks) == ["x", "y", "z"]


if __name__ == "__main__":
    _checks()
    print("chapitre 26 — corrigés OK")
