"""Chapitre 8 — Erreurs, exceptions et modules : corrigés."""

from __future__ import annotations

import json


# ---------------------------------------------------------------------------
# Exercice 1 — Refaire : rendre l'except spécifique
# ---------------------------------------------------------------------------
def parse_user(raw: str) -> tuple[str, int]:
    """N'attrape que les exceptions attendues ; laisse remonter l'imprévu."""
    try:
        data = json.loads(raw)        # JSONDecodeError
        user = data["user"]           # KeyError
        age = int(data["age"])        # KeyError ou ValueError
    except (json.JSONDecodeError, KeyError, ValueError):
        return "anonymous", 0
    return user, age


# ---------------------------------------------------------------------------
# Exercice 2 — Comprendre : EAFP ou LBYL
# ---------------------------------------------------------------------------
def get_timeout_lbyl(config: dict[str, int]) -> int:
    return config["timeout"] if "timeout" in config else 30


def get_timeout_eafp(config: dict[str, int]) -> int:
    try:
        return config["timeout"]
    except KeyError:
        return 30


def get_timeout_idiomatic(config: dict[str, int]) -> int:
    """Le plus direct pour un défaut de dict : dict.get (atomique)."""
    return config.get("timeout", 30)


# ---------------------------------------------------------------------------
# Exercice 3 — Concevoir : la politique d'erreurs de Taskline
# ---------------------------------------------------------------------------
class TasklineError(Exception):
    """Base commune : permet d'attraper « toute erreur du domaine »."""


class TaskNotFound(TasklineError):
    """Levée dans la couche d'accès aux données ; attrapée au point d'entrée
    (404 d'une API)."""


class InvalidTaskData(TasklineError):
    """Levée à la frontière (validation) ; attrapée là où l'on formule la
    réponse d'erreur."""


class PermissionDenied(TasklineError):
    """Levée dans la couche métier ; attrapée au point d'entrée (403)."""


def get_task(store: dict[int, str], task_id: int) -> str:
    """Lève au point de détection ; l'appelant décide où attraper."""
    try:
        return store[task_id]
    except KeyError:
        raise TaskNotFound(f"no task {task_id}") from None


def _checks() -> None:
    assert parse_user('{"user": "ada", "age": "42"}') == ("ada", 42)
    assert parse_user("not json") == ("anonymous", 0)
    assert parse_user('{"user": "ada"}') == ("anonymous", 0)

    cfg = {"timeout": 5}
    assert get_timeout_lbyl(cfg) == 5
    assert get_timeout_eafp({}) == 30
    assert get_timeout_idiomatic({}) == 30

    store = {1: "write"}
    assert get_task(store, 1) == "write"
    try:
        get_task(store, 99)
    except TaskNotFound as exc:
        assert isinstance(exc, TasklineError)   # base commune
    else:
        raise AssertionError("TaskNotFound attendue")


if __name__ == "__main__":
    _checks()
    print("chapitre 8 — corrigés OK")
