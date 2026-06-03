"""Chapitre 11 — Les annotations de type : corrigés.

Ces corrigés sont surtout des signatures. On les vérifie via leur
comportement à l'exécution (un vérificateur statique comme ty/mypy
confirmerait la cohérence des types avant l'exécution).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Task:
    id: int
    title: str
    owner: str | None = None


# ---------------------------------------------------------------------------
# Exercice 1 — Refaire : annoter une signature
# ---------------------------------------------------------------------------
def assign(
    store: dict[int, Task],
    task_id: int,
    user: str | None = None,
) -> Task | None:
    """Retour `Task | None` car la fonction renvoie None si absente — mentir
    avec `-> Task` serait pire que rien."""
    task = store.get(task_id)
    if task is None:
        return None
    task.owner = user
    return task


# ---------------------------------------------------------------------------
# Exercice 2 — Comprendre : pourquoi le vérificateur se plaint (narrowing)
# ---------------------------------------------------------------------------
def first_word(text: str | None) -> str:
    """`text` peut être None : on traite le cas (narrowing), pas `Any`."""
    if text is None:
        return ""               # décider ce que « pas de texte » signifie
    return text.split()[0]


# ---------------------------------------------------------------------------
# Exercice 3 — Concevoir : typer la frontière de Taskline
# ---------------------------------------------------------------------------
type RawJson = dict[str, object]    # honnête : valeurs inconnues, mais typées


def import_tasks(raw: list[RawJson]) -> list[Task]:
    """Entrée non fiable typée `dict[str, object]` (force à valider) ;
    sortie précise `list[Task]` : l'intérieur redevient sûr."""
    tasks: list[Task] = []
    for item in raw:
        tasks.append(Task(id=int(item["id"]), title=str(item["title"])))  # type: ignore[arg-type]
    return tasks


def _checks() -> None:
    store = {1: Task(1, "write")}
    assert assign(store, 1, "ada").owner == "ada"  # type: ignore[union-attr]
    assert assign(store, 99) is None

    assert first_word(None) == ""
    assert first_word("hello world") == "hello"

    out = import_tasks([{"id": 1, "title": "write"}, {"id": 2, "title": "test"}])
    assert [t.id for t in out] == [1, 2]


if __name__ == "__main__":
    _checks()
    print("chapitre 11 — corrigés OK")
