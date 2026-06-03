"""Chapitre 10 — Le style qui se lit : corrigés."""

from __future__ import annotations

from dataclasses import dataclass


# ---------------------------------------------------------------------------
# Exercice 1 — Refaire : renommer pour clarifier (sans commentaire)
# ---------------------------------------------------------------------------
@dataclass
class Task:
    value: int


def above_threshold(tasks: list[Task], threshold: int) -> list[Task]:
    """Le nom des choses EST la documentation : plus de commentaire utile."""
    return [task for task in tasks if task.value > threshold]


# ---------------------------------------------------------------------------
# Exercice 2 — Comprendre : signal ou bruit
# ---------------------------------------------------------------------------
# Pour chaque commentaire : "signal" (un POURQUOI utile) ou "bruit" (répète le quoi).
EXERCICE_2 = {
    "a) count = 0  # initialize count to zero": "bruit",
    "b) retries = 5  # the gateway drops the 6th attempt": "signal",
    "c) x = x * 2  # double x": "bruit",
    "d) time.sleep(1)  # avoid hammering the flaky upstream": "signal",
}


# ---------------------------------------------------------------------------
# Exercice 3 — Concevoir : une convention d'équipe
# ---------------------------------------------------------------------------
EXERCICE_3 = """\
Convention : fonctions en snake_case, ordre verbe + nom (get_user,
create_task, list_overdue) ; classes en PascalCase ; « privé » préfixé d'un
underscore (_cache).
Outillage : activer les règles de nommage de Ruff (famille N, pep8-naming)
dans pyproject.toml et faire échouer la CI si une convention est violée.
On déplace la cohérence de l'humain (faillible) vers la machine (constante).
"""


def _checks() -> None:
    tasks = [Task(3), Task(10), Task(7)]
    assert above_threshold(tasks, 5) == [Task(10), Task(7)]
    assert list(EXERCICE_2.values()) == ["bruit", "signal", "bruit", "signal"]


if __name__ == "__main__":
    _checks()
    print("chapitre 10 — corrigés OK")
