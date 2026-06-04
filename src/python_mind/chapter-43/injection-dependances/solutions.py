"""Chapitre 43 — Injection de dépendances et assemblage du système : corrigés."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


# ---------------------------------------------------------------------------
# Exercice 1 — Refaire : injecter au lieu de souder
# ---------------------------------------------------------------------------
class OrderRepository(Protocol):
    def save(self, amount: int) -> None: ...


class Mailer(Protocol):
    def send(self, msg: str) -> None: ...


class OrderService:
    """Dépendances reçues par le constructeur (explicites, remplaçables)."""

    def __init__(self, repo: OrderRepository, mailer: Mailer) -> None:
        self.repo = repo
        self.mailer = mailer

    def place(self, amount: int) -> None:
        self.repo.save(amount)
        self.mailer.send(f"order {amount}")


# ---------------------------------------------------------------------------
# Exercice 2 — Comprendre : la dépendance cachée
# ---------------------------------------------------------------------------
EXERCICE_2 = """\
Une méthode qui lit un Singleton global lit GLOBAL_DB au fond de son corps :
pour la tester, il faut MANIPULER l'état global (le remplacer, le réinitialiser
entre tests), fragile et source de tests interdépendants. Avec l'injection,
on passe simplement le faux ; le test est local et sans effet de bord.
"""


# ---------------------------------------------------------------------------
# Exercice 3 — Concevoir : la composition root de Taskline
# ---------------------------------------------------------------------------
@dataclass
class Settings:
    repo_kind: str = "memory"


class TaskRepository(Protocol):
    def add(self, title: str) -> None: ...
    def all(self) -> list[str]: ...


class InMemoryRepo:
    def __init__(self) -> None:
        self._titles: list[str] = []

    def add(self, title: str) -> None:
        self._titles.append(title)

    def all(self) -> list[str]:
        return list(self._titles)


def make_repo(settings: Settings) -> TaskRepository:
    return {"memory": InMemoryRepo}[settings.repo_kind]()


class TaskService:
    def __init__(self, repo: TaskRepository) -> None:
        self._repo = repo           # ne dépend QUE de l'abstraction

    def add_task(self, title: str) -> None:
        self._repo.add(title)

    def titles(self) -> list[str]:
        return self._repo.all()


def build_service(settings: Settings) -> TaskService:
    """Composition root : on assemble le graphe concret EN UN SEUL endroit."""
    return TaskService(repo=make_repo(settings))


def make_test_service() -> TaskService:
    """En test : on injecte directement un faux, sans le vrai câblage."""
    return TaskService(repo=InMemoryRepo())


def _checks() -> None:
    saved: list[int] = []
    sent: list[str] = []

    class FakeRepo:
        def save(self, amount: int) -> None:
            saved.append(amount)

    class FakeMailer:
        def send(self, msg: str) -> None:
            sent.append(msg)

    OrderService(FakeRepo(), FakeMailer()).place(42)
    assert saved == [42] and sent == ["order 42"]

    # Prod (assemblé à la composition root) et test partagent le MÊME service,
    # seul le point d'assemblage change.
    prod = build_service(Settings())
    prod.add_task("write")
    assert prod.titles() == ["write"]

    test = make_test_service()
    test.add_task("x")
    assert test.titles() == ["x"]   # isolé, aucun état partagé


if __name__ == "__main__":
    _checks()
    print("chapitre 43 — corrigés OK")
