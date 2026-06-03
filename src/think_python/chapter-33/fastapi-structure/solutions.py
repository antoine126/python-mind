"""Chapitre 33 — Dépendances, async et structure d'un projet FastAPI : corrigés.

Nécessite l'extra « web » : ``uv sync --extra web``.
Illustre l'architecture en couches (route -> service -> dépôt) et l'injection
de dépendances (Depends), testée sans vraie base via dependency_overrides.
"""

from __future__ import annotations

from dataclasses import dataclass

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field


# --- Cœur + couches ---------------------------------------------------------
@dataclass
class Task:
    id: int
    title: str


class TasklineError(Exception):
    pass


class TaskNotFound(TasklineError):
    pass


class TooManyTasks(TasklineError):
    pass


class InMemoryTaskRepo:                 # dépôt (accès données)
    def __init__(self) -> None:
        self._tasks: dict[int, Task] = {}
        self._next_id = 1

    def add(self, title: str) -> Task:
        task = Task(self._next_id, title)
        self._tasks[task.id] = task
        self._next_id += 1
        return task

    def get(self, task_id: int) -> Task:
        try:
            return self._tasks[task_id]
        except KeyError:
            raise TaskNotFound(str(task_id)) from None

    def count(self) -> int:
        return len(self._tasks)


class TaskService:                      # métier (règles, orchestration)
    def __init__(self, repo: InMemoryTaskRepo) -> None:
        self._repo = repo

    def create(self, title: str) -> Task:
        if self._repo.count() >= 100:
            raise TooManyTasks()        # règle métier
        return self._repo.add(title)

    def get(self, task_id: int) -> Task:
        return self._repo.get(task_id)


# --- Frontière HTTP ---------------------------------------------------------
class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=80)


class TaskOut(BaseModel):
    id: int
    title: str


app = FastAPI(title="Taskline — chapitre 33")
_repo = InMemoryTaskRepo()              # composition root (simplifiée)


def get_service() -> TaskService:       # provider injecté
    return TaskService(repo=_repo)


@app.post("/tasks", status_code=201, response_model=TaskOut)
def create_task(
    payload: TaskCreate, service: TaskService = Depends(get_service)
) -> Task:
    try:
        return service.create(payload.title)   # la route délègue au service
    except TooManyTasks:
        raise HTTPException(429, "too many tasks")


@app.get("/tasks/{task_id}", response_model=TaskOut)
def read_task(
    task_id: int, service: TaskService = Depends(get_service)
) -> Task:
    try:
        return service.get(task_id)
    except TaskNotFound:
        raise HTTPException(404, "task not found")


# Exercice 1 — la version « tout dans la route » a été découpée ci-dessus :
# route (frontière) -> service (métier) -> dépôt (données). Chaque couche est
# testable seule.
# Exercice 2 — l'injection rend la route testable SANS base : on remplace le
# provider par un faux via app.dependency_overrides (cf. _checks).


def _checks() -> None:
    from fastapi.testclient import TestClient

    # On injecte un dépôt en mémoire NEUF pour le test (pas d'état partagé).
    fresh = InMemoryTaskRepo()
    app.dependency_overrides[get_service] = lambda: TaskService(repo=fresh)
    try:
        client = TestClient(app)
        resp = client.post("/tasks", json={"title": "write"})
        assert resp.status_code == 201
        task_id = resp.json()["id"]
        assert client.get(f"/tasks/{task_id}").json()["title"] == "write"
        assert client.get("/tasks/999").status_code == 404   # TaskNotFound -> 404
    finally:
        app.dependency_overrides.clear()


if __name__ == "__main__":
    _checks()
    print("chapitre 33 — corrigés OK")
