"""Chapitre 20 — Abstractions : ABC, Protocols et duck typing : corrigés."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


# ---------------------------------------------------------------------------
# Exercice 1 — Refaire : du test de type au comportement (polymorphisme)
# ---------------------------------------------------------------------------
class Circle:
    def __init__(self, radius: float) -> None:
        self.radius = radius

    def area(self) -> float:
        return 3.14 * self.radius**2


class Square:
    def __init__(self, side: float) -> None:
        self.side = side

    def area(self) -> float:
        return self.side**2


def area(shape: object) -> float:
    """Duck typing : tout objet ayant .area() convient (pas de test de type)."""
    return shape.area()  # type: ignore[attr-defined]


# ---------------------------------------------------------------------------
# Exercice 2 — Comprendre : Protocol ou ABC
# ---------------------------------------------------------------------------
EXERCICE_2 = {
    "a) objet « fichier-like » tiers": "Protocol — accepter toute classe (y "
    "compris tierce) ayant read(), sans héritage : seul le structurel marche.",
    "b) famille de Repository avec get_or_raise concret": "ABC — comportement "
    "partagé concret + contrat abstrait (find), et instanciation forcée.",
}


# ---------------------------------------------------------------------------
# Exercice 3 — Concevoir : un contrat de stockage pour Taskline
# ---------------------------------------------------------------------------
@dataclass
class Task:
    id: int
    title: str


class TaskRepository(Protocol):       # contrat structurel, sans héritage
    def add(self, task: Task) -> None: ...
    def get(self, task_id: int) -> Task: ...
    def all(self) -> list[Task]: ...


class InMemoryRepo:                    # satisfait le Protocol SANS en hériter
    def __init__(self) -> None:
        self._d: dict[int, Task] = {}

    def add(self, task: Task) -> None:
        self._d[task.id] = task

    def get(self, task_id: int) -> Task:
        return self._d[task_id]

    def all(self) -> list[Task]:
        return list(self._d.values())


class TaskService:
    """Le code métier ne dépend que de la FORME TaskRepository."""

    def __init__(self, repo: TaskRepository) -> None:
        self._repo = repo

    def add_task(self, task_id: int, title: str) -> None:
        self._repo.add(Task(task_id, title))

    def titles(self) -> list[str]:
        return [t.title for t in self._repo.all()]


def _checks() -> None:
    assert round(area(Circle(2)), 2) == 12.56
    assert area(Square(3)) == 9

    service = TaskService(repo=InMemoryRepo())   # faux injecté, sans héritage
    service.add_task(1, "write")
    service.add_task(2, "test")
    assert service.titles() == ["write", "test"]


if __name__ == "__main__":
    _checks()
    print("chapitre 20 — corrigés OK")
