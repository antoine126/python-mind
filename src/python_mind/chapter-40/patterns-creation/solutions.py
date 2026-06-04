"""Chapitre 40 — Patterns de création : corrigés."""

from __future__ import annotations

from typing import Protocol


# ---------------------------------------------------------------------------
# Exercice 1 — Refaire : fabrique extensible (registre)
# ---------------------------------------------------------------------------
class Notifier(Protocol):
    def send(self, msg: str) -> str: ...


class EmailNotifier:
    def send(self, msg: str) -> str:
        return f"email: {msg}"


class SmsNotifier:
    def send(self, msg: str) -> str:
        return f"sms: {msg}"


class SlackNotifier:               # ajout = une entrée, fabrique intacte
    def send(self, msg: str) -> str:
        return f"slack: {msg}"


_NOTIFIERS: dict[str, type[Notifier]] = {
    "email": EmailNotifier,
    "sms": SmsNotifier,
    "slack": SlackNotifier,
}


def make_notifier(kind: str) -> Notifier:
    try:
        return _NOTIFIERS[kind]()
    except KeyError:
        raise ValueError(f"unknown notifier {kind}") from None


# ---------------------------------------------------------------------------
# Exercice 2 — Comprendre : Singleton ou injection
# ---------------------------------------------------------------------------
EXERCICE_2 = """\
Problèmes du Singleton global de cache :
1. État partagé ENTRE TESTS — le cache rempli par un test fuit dans le suivant
   (tests interdépendants, ordre significatif).
2. Impossible de SUBSTITUER un faux sans bidouiller l'état global.
Version injectée : chaque test fournit un cache neuf, aucune fuite.
"""


class Cache(Protocol):
    def get(self, key: str) -> int | None: ...
    def set(self, key: str, value: int) -> None: ...


class FakeCache:
    def __init__(self) -> None:
        self._d: dict[str, int] = {}

    def get(self, key: str) -> int | None:
        return self._d.get(key)

    def set(self, key: str, value: int) -> None:
        self._d[key] = value


class TaskService:
    def __init__(self, cache: Cache) -> None:
        self._cache = cache         # injecté, remplaçable en test


# ---------------------------------------------------------------------------
# Exercice 3 — Concevoir : créer des dépôts selon la config (fabrique + injection)
# ---------------------------------------------------------------------------
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


# (JsonRepo, SqlRepo auraient la même forme.)
_REPOS: dict[str, type[TaskRepository]] = {"memory": InMemoryRepo}


def make_repo(repo_kind: str) -> TaskRepository:
    return _REPOS[repo_kind]()      # la fabrique décide QUEL dépôt


class Service:
    def __init__(self, repo: TaskRepository) -> None:
        self._repo = repo           # l'injection le BRANCHE (création découplée)

    def add(self, title: str) -> None:
        self._repo.add(title)

    def titles(self) -> list[str]:
        return self._repo.all()


def _checks() -> None:
    assert make_notifier("email").send("hi") == "email: hi"
    assert make_notifier("slack").send("hi") == "slack: hi"
    try:
        make_notifier("carrier-pigeon")
    except ValueError:
        pass
    else:
        raise AssertionError("ValueError attendue (notifier inconnu)")

    TaskService(FakeCache())        # injection : pas de Singleton global

    repo = make_repo("memory")      # fabrique selon la config
    service = Service(repo=repo)    # injecté
    service.add("write")
    assert service.titles() == ["write"]


if __name__ == "__main__":
    _checks()
    print("chapitre 40 — corrigés OK")
