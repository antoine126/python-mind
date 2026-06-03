"""Chapitre 32 — FastAPI : des routes typées et validées : corrigés.

Nécessite l'extra « web » : ``uv sync --extra web``.
Lancer le serveur : ``uv run uvicorn solutions:app --reload`` (depuis ce dossier).
"""

from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Taskline — chapitre 32")


# ---------------------------------------------------------------------------
# Exercice 1 — Refaire : typer une route (et ne pas fuiter le mot de passe)
# ---------------------------------------------------------------------------
class UserCreate(BaseModel):
    name: str = Field(min_length=1)
    pw: str = Field(min_length=8)


class UserOut(BaseModel):          # pas de champ password : il est filtré
    id: int
    name: str


@app.post("/users", status_code=201, response_model=UserOut)
def create_user(payload: UserCreate) -> dict:
    # response_model=UserOut retire automatiquement le mot de passe de la réponse
    return {"id": 1, "name": payload.name, "pw": payload.pw}


# ---------------------------------------------------------------------------
# Exercice 3 — Concevoir : l'endpoint de création de Taskline
# ---------------------------------------------------------------------------
class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=80)
    priority: int = Field(default=1, ge=1, le=5)


class TaskOut(BaseModel):
    id: int
    title: str
    priority: int
    done: bool


@app.post("/tasks", status_code=201, response_model=TaskOut)
def create_task(payload: TaskCreate) -> dict:
    return {"id": 1, "title": payload.title, "priority": payload.priority, "done": False}


# Exercice 2 — Comprendre : d'où vient le 422 ?
EXERCICE_2 = """\
L'annotation `task_id: int` dit à FastAPI que ce paramètre de chemin est un
entier. FastAPI tente de convertir "abc" en int ; l'échec est une erreur de
validation de l'ENTRÉE (côté client), traduite en 422 — sans que vous écriviez
la moindre validation. C'est le 4xx « faute du client ».
"""


@app.get("/tasks/{task_id}")
def read_task(task_id: int) -> dict:    # /tasks/abc -> 422 automatique
    return {"id": task_id}


def _checks() -> None:
    from fastapi.testclient import TestClient

    client = TestClient(app)

    # Le mot de passe n'apparaît PAS dans la réponse (filtré par UserOut).
    resp = client.post("/users", json={"name": "ada", "pw": "secret123"})
    assert resp.status_code == 201
    assert resp.json() == {"id": 1, "name": "ada"}
    assert "pw" not in resp.json()

    # Création de tâche : coercition + statut 201.
    resp = client.post("/tasks", json={"title": "write", "priority": "3"})
    assert resp.status_code == 201
    assert resp.json()["priority"] == 3

    # Entrées invalides -> 422.
    assert client.post("/tasks", json={"title": ""}).status_code == 422
    assert client.get("/tasks/abc").status_code == 422


if __name__ == "__main__":
    _checks()
    print("chapitre 32 — corrigés OK")
