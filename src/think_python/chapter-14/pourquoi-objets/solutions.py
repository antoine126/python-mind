"""Chapitre 14 — Pourquoi (et quand) des objets ? : corrigés."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date


# ---------------------------------------------------------------------------
# Exercice 1 — Refaire : dégonfler une classe inutile
# ---------------------------------------------------------------------------
# La classe Validator n'avait aucun état : c'était une fonction.
def is_valid_email(s: str) -> bool:
    return "@" in s and "." in s


# ---------------------------------------------------------------------------
# Exercice 2 — Comprendre : objet ou fonction
# ---------------------------------------------------------------------------
EXERCICE_2 = {
    "a) Celsius -> Fahrenheit": "fonction (transformation pure, sans état)",
    "b) panier d'achat": "classe (état = articles + comportement = total)",
    "c) utilitaires de dates": "module (fonctions apparentées, sans état)",
    "d) connexion réseau": "classe (état + cycle de vie ; cf. context manager)",
}


# ---------------------------------------------------------------------------
# Exercice 3 — Concevoir : modéliser Taskline
# ---------------------------------------------------------------------------
@dataclass            # données : ni fonction, ni classe nue
class Task:
    title: str
    due: date | None = None
    done: bool = False


class TaskStore:      # état + comportement => classe
    def __init__(self) -> None:
        self._tasks: dict[int, Task] = {}
        self._next_id = 1

    def add(self, task: Task) -> int:
        task_id = self._next_id
        self._tasks[task_id] = task
        self._next_id += 1
        return task_id

    def get(self, task_id: int) -> Task:
        return self._tasks[task_id]

    def remove(self, task_id: int) -> None:
        del self._tasks[task_id]

    def all(self) -> list[Task]:
        return list(self._tasks.values())


def sort_by_due(tasks: list[Task]) -> list[Task]:   # tri : fonction pure
    return sorted(tasks, key=lambda t: t.due or date.max)


def _checks() -> None:
    assert is_valid_email("a@b.com")
    assert not is_valid_email("nope")

    store = TaskStore()
    a = store.add(Task("write", date(2026, 6, 2)))
    store.add(Task("test", date(2026, 6, 1)))
    assert store.get(a).title == "write"
    assert [t.title for t in sort_by_due(store.all())] == ["test", "write"]
    store.remove(a)
    assert len(store.all()) == 1


if __name__ == "__main__":
    _checks()
    print("chapitre 14 — corrigés OK")
