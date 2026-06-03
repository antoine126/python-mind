"""Chapitre 12 — Tester : la confiance par la preuve : corrigés.

Le code « sous test » (SUT) vit ici ; les tests pytest illustratifs sont dans
``test_billing.py`` (même dossier). ``_checks()`` reprend les vérifications.
"""

from __future__ import annotations

from dataclasses import dataclass, field


# --- Système sous test ------------------------------------------------------
def with_tax(amount: int, rate: float) -> float:
    """Applique un taux de TVA ; refuse un taux négatif."""
    if rate < 0:
        raise ValueError("rate must be >= 0")
    return amount * (1 + rate)


@dataclass
class Task:
    title: str
    id: int = 0


@dataclass
class TaskStore:
    _tasks: dict[int, Task] = field(default_factory=dict)
    _next_id: int = 1

    def add(self, task: Task) -> Task:
        task.id = self._next_id
        self._tasks[task.id] = task
        self._next_id += 1
        return task

    def get(self, task_id: int) -> Task:
        return self._tasks[task_id]

    def count(self) -> int:
        return len(self._tasks)

    def titles(self) -> list[str]:
        return [t.title for t in self._tasks.values()]


# ---------------------------------------------------------------------------
# Exercice 2 — Comprendre : pourquoi ce test est fragile
# ---------------------------------------------------------------------------
EXERCICE_2 = """\
Le test d'origine lit `store._tasks[-1]`, un détail privé (liste indexable).
Si l'implémentation passe à un dict, `_tasks[-1]` n'a plus de sens et le test
casse — alors que « ajouter une tâche la rend récupérable » reste vrai.
Version robuste : tester par l'API publique (add/get), pas l'interne.
"""


def _checks() -> None:
    # Exercice 1 — un test structuré Arrange-Act-Assert (ici, via le SUT).
    store = TaskStore()
    store.add(Task("a"))
    store.add(Task("b"))
    assert store.count() == 2
    assert "a" in store.titles()

    # Exercice 2 — comportement testé par l'API publique (pas l'interne).
    store2 = TaskStore()
    task = store2.add(Task("write"))
    assert store2.get(task.id).title == "write"

    # Exercice 3 — table de cas valides + l'exception à part.
    cases = [(100, 0.2, 120), (0, 0.2, 0), (100, 0.0, 100), (100, 1.0, 200)]
    for amount, rate, expected in cases:
        assert with_tax(amount, rate) == expected
    try:
        with_tax(100, rate=-0.1)
    except ValueError:
        pass
    else:
        raise AssertionError("ValueError attendue pour un taux négatif")


if __name__ == "__main__":
    _checks()
    print("chapitre 12 — corrigés OK")
