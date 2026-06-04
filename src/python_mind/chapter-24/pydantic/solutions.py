"""Chapitre 24 — Pydantic : valider aux frontières : corrigés.

Nécessite l'extra « web » : ``uv sync --extra web``.
Le harnais de tests ignore ce fichier si Pydantic n'est pas installé.
"""

from __future__ import annotations

from dataclasses import dataclass

from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------------------------
# Exercice 1 — Refaire : valider une entrée
# ---------------------------------------------------------------------------
class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")     # rejette les champs inconnus
    title: str = Field(min_length=1, max_length=80)
    priority: int = Field(default=1, ge=1, le=5)


# ---------------------------------------------------------------------------
# Exercice 2 — Comprendre : pourquoi la coercition surprend
# ---------------------------------------------------------------------------
EXERCICE_2 = """\
Pydantic tente une COERCITION guidée par le type annoté. Pour un champ int,
il convertit "3" -> 3 (cas classique d'un JSON laxiste), mais refuse "high"
(non convertible) avec une ValidationError. C'est souhaitable à la frontière :
les données externes arrivent souvent mal typées ; on NORMALISE une fois vers
les bons types tout en REJETANT l'absurde.
"""


# ---------------------------------------------------------------------------
# Exercice 3 — Concevoir : la membrane de Taskline
# ---------------------------------------------------------------------------
class TaskOut(BaseModel):              # frontière de SORTIE
    id: int
    title: str
    priority: int
    done: bool


@dataclass                             # cœur (de confiance)
class Task:
    id: int
    title: str
    priority: int
    done: bool = False


def create(raw: str) -> Task:
    """JSON brut -> TaskCreate (validé, point unique) -> Task (cœur)."""
    payload = TaskCreate.model_validate_json(raw)
    return Task(id=1, title=payload.title, priority=payload.priority)


def serialize(task: Task) -> str:
    return TaskOut(**task.__dict__).model_dump_json()


def _checks() -> None:
    from pydantic import ValidationError

    # Coercition à la frontière : "3" -> 3.
    t = TaskCreate.model_validate({"title": "write", "priority": "3"})
    assert t.priority == 3

    # Rejets : titre vide, priorité hors bornes, champ inconnu, type absurde.
    for bad in (
        {"title": ""},
        {"title": "x", "priority": 99},
        {"title": "x", "unknown": 1},
        {"title": "x", "priority": "high"},
    ):
        try:
            TaskCreate.model_validate(bad)
        except ValidationError:
            pass
        else:
            raise AssertionError(f"ValidationError attendue pour {bad}")

    task = create('{"title": "write", "priority": "3"}')
    assert task == Task(1, "write", 3)
    assert '"title":"write"' in serialize(task)


if __name__ == "__main__":
    _checks()
    print("chapitre 24 — corrigés OK")
