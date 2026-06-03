"""Chapitre 21 — Le paysage : classe nue, dataclass, NamedTuple, TypedDict,
Pydantic : corrigés.

On illustre les outils de la bibliothèque standard (NamedTuple, dataclass,
TypedDict). Pydantic (la frontière) est traité au chapitre 24.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import NamedTuple, TypedDict


# ---------------------------------------------------------------------------
# Exercice 1 — Refaire : choisir l'outil
# ---------------------------------------------------------------------------
EXERCICE_1 = {
    "a) corps JSON d'une requête": "Pydantic — frontière, à valider",
    "b) paire (lat, lon) interne immuable": "NamedTuple — immuable, léger",
    "c) Account avec invariant + méthodes": "classe nue — comportement riche",
    "d) forme d'un dict de config": "TypedDict — la forme, sans créer d'objet",
}


# (b) NamedTuple : enregistrement immuable léger
class Point(NamedTuple):
    lat: float
    lon: float


# (d) TypedDict : la forme d'un dict (pas d'objet ni de méthode)
class ConfigShape(TypedDict):
    host: str
    port: int


# ---------------------------------------------------------------------------
# Exercice 2 — Comprendre : pourquoi pas Pydantic ici
# ---------------------------------------------------------------------------
EXERCICE_2 = """\
Deux raisons de réserver Pydantic à la frontière :
1. COÛT — Pydantic valide à chaque instanciation ; pour des millions d'objets
   internes triviaux déjà sûrs, c'est du CPU gaspillé.
2. COUPLAGE — tout le cœur dépendrait d'une dépendance externe, là où une
   dataclass (stdlib) suffit, et les tests s'en trouvent compliqués.
Exception : revalider au franchissement d'une NOUVELLE frontière de confiance
(sortie d'une file de messages, avant une base partagée).
"""


# ---------------------------------------------------------------------------
# Exercice 3 — Concevoir : la frontière de Taskline
# ---------------------------------------------------------------------------
# Frontière (validée) ; au chapitre 24 ce serait un BaseModel Pydantic.
def validate_task_create(raw: dict) -> dict:
    title = str(raw.get("title", "")).strip()
    if not (1 <= len(title) <= 80):
        raise ValueError("title must be 1..80 chars")
    priority = int(raw.get("priority", 1))
    if not 1 <= priority <= 5:
        raise ValueError("priority must be 1..5")
    return {"title": title, "priority": priority}


@dataclass        # cœur : objet de confiance
class Task:
    title: str
    priority: int


def create(raw: dict) -> Task:
    """Flux : brut -> validé (membrane) -> Task (cœur), validé UNE seule fois."""
    data = validate_task_create(raw)        # point unique de validation
    return Task(title=data["title"], priority=data["priority"])


def _checks() -> None:
    p = Point(48.85, 2.35)
    assert p.lat == 48.85 and tuple(p) == (48.85, 2.35)
    cfg: ConfigShape = {"host": "localhost", "port": 8000}
    assert cfg["port"] == 8000

    task = create({"title": "write", "priority": "3"})  # "3" converti à l'entrée
    assert task == Task("write", 3)
    for bad in ({"title": ""}, {"title": "x", "priority": 99}):
        try:
            create(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("ValueError attendue à la frontière")


if __name__ == "__main__":
    _checks()
    print("chapitre 21 — corrigés OK")
