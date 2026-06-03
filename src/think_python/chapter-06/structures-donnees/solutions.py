"""Chapitre 6 — Structures de données et le bon choix : corrigés."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Exercice 1 — Refaire : choisir la structure
# ---------------------------------------------------------------------------
EXERCICE_1 = {
    "a": "set (ou Counter pour aussi compter) — unicité",
    "b": "dict — accès par clé",
    "c": "list (ou collections.deque si on retire en tête) — ordre",
    "d": "tuple — paire figée",
}


def mots_uniques(texte: str) -> set[str]:
    return set(texte.split())


def compter_mots(texte: str) -> Counter[str]:
    return Counter(texte.split())


# ---------------------------------------------------------------------------
# Exercice 2 — Comprendre : pourquoi c'est lent (O(n²) -> O(n))
# ---------------------------------------------------------------------------
def dedup(items: list[int]) -> list[int]:
    """Déduplication en O(n) : un set pour l'appartenance, une liste pour l'ordre."""
    seen: set[int] = set()
    unique: list[int] = []
    for x in items:
        if x not in seen:        # O(1)
            seen.add(x)
            unique.append(x)
    return unique


# ---------------------------------------------------------------------------
# Exercice 3 — Concevoir : un index pour Taskline
# ---------------------------------------------------------------------------
@dataclass
class Task:
    id: int
    title: str
    tags: set[str] = field(default_factory=set)


class TaskIndex:
    """Plusieurs vues d'une même donnée, maintenues synchronisées.

    Coût : mémoire supplémentaire + discipline (toute écriture met à jour
    TOUS les index), en échange de lectures O(1).
    """

    def __init__(self) -> None:
        self._by_id: dict[int, Task] = {}
        self._all_labels: set[str] = set()

    def add(self, task: Task) -> None:
        self._by_id[task.id] = task
        self._all_labels |= task.tags

    def exists(self, task_id: int) -> bool:      # O(1)
        return task_id in self._by_id

    def get(self, task_id: int) -> Task:         # O(1)
        return self._by_id[task_id]

    def labels(self) -> set[str]:
        return set(self._all_labels)


def _checks() -> None:
    assert mots_uniques("a b a c") == {"a", "b", "c"}
    assert compter_mots("a b a c")["a"] == 2

    assert dedup([3, 1, 3, 2, 1]) == [3, 1, 2]

    index = TaskIndex()
    index.add(Task(1, "write", {"urgent"}))
    index.add(Task(2, "test", {"backend"}))
    assert index.exists(1) and not index.exists(99)
    assert index.get(2).title == "test"
    assert index.labels() == {"urgent", "backend"}


if __name__ == "__main__":
    _checks()
    print("chapitre 6 — corrigés OK")
