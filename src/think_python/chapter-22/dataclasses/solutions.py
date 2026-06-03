"""Chapitre 22 — Les dataclasses en profondeur : corrigés."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date


# ---------------------------------------------------------------------------
# Exercice 1 — Refaire : de la classe nue à la dataclass (immuable)
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Point:
    x: int
    y: int


# ---------------------------------------------------------------------------
# Exercice 2 — Comprendre : le défaut partagé
# ---------------------------------------------------------------------------
# `items: list[str] = []` lève une ValueError à la définition ; on utilise
# default_factory pour une liste neuve par instance.
@dataclass
class Cart:
    items: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Exercice 3 — Concevoir : une tâche immuable triable
# ---------------------------------------------------------------------------
@dataclass(frozen=True, order=True, slots=True)
class Task:
    due: date                                   # comparé en premier
    priority: int                               # puis la priorité
    title: str = field(compare=False)           # hors comparaison
    tags: tuple[str, ...] = field(              # tuple => immuable/hashable
        default_factory=tuple, compare=False
    )

    def __post_init__(self) -> None:
        if not self.title:
            raise ValueError("title cannot be empty")


def _checks() -> None:
    p = Point(1, 2)
    assert p == Point(1, 2)
    assert {p}                                   # frozen => hashable
    try:
        p.x = 5  # type: ignore[misc]
    except Exception:
        pass
    else:
        raise AssertionError("FrozenInstanceError attendue")

    a, b = Cart(), Cart()
    a.items.append("apple")
    assert a.items == ["apple"] and b.items == []   # pas de partage

    t1 = Task(date(2026, 6, 2), 3, "b")
    t2 = Task(date(2026, 6, 1), 1, "a")
    assert sorted([t1, t2])[0] is t2                # trié par échéance
    assert {t1}                                     # hashable
    try:
        Task(date.today(), 1, "")
    except ValueError:
        pass
    else:
        raise AssertionError("ValueError attendue (titre vide)")


if __name__ == "__main__":
    _checks()
    print("chapitre 22 — corrigés OK")
