"""Chapitre 27 — Décorateurs : corrigés."""

from __future__ import annotations

import functools
from collections.abc import Callable
from typing import Any


# ---------------------------------------------------------------------------
# Exercice 1 — Refaire : un décorateur de log
# ---------------------------------------------------------------------------
def logged(fn: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(fn)               # préserve nom/docstring/signature
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        wrapper.calls.append((args, kwargs))   # type: ignore[attr-defined]
        return fn(*args, **kwargs)              # ne pas oublier de renvoyer !

    wrapper.calls = []                 # type: ignore[attr-defined]
    return wrapper


# ---------------------------------------------------------------------------
# Exercice 2 — Comprendre : l'identité perdue (la correction en une ligne)
# ---------------------------------------------------------------------------
def timed(fn: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(fn)               # <- la correction : préserve __name__
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return fn(*args, **kwargs)

    return wrapper


# ---------------------------------------------------------------------------
# Exercice 3 — Concevoir : un décorateur d'autorisation
# ---------------------------------------------------------------------------
class PermissionDenied(Exception):
    pass


class User:
    def __init__(self, user_id: int, is_admin: bool) -> None:
        self.id = user_id
        self.is_admin = is_admin


def require_admin(fn: Callable[..., Any]) -> Callable[..., Any]:
    """Contrôle d'accès (transversal) AVANT l'exécution ; pas de logique métier."""

    @functools.wraps(fn)
    def wrapper(user: User, *args: Any, **kwargs: Any) -> Any:
        if not user.is_admin:
            raise PermissionDenied(f"{user.id} is not admin")
        return fn(user, *args, **kwargs)

    return wrapper


@require_admin
def delete_all(user: User) -> str:
    return "deleted"


def _checks() -> None:
    @logged
    def add(a: int, b: int) -> int:
        """Add two numbers."""
        return a + b

    assert add(2, 3) == 5
    assert add.__name__ == "add"            # identité préservée
    assert add.__doc__ == "Add two numbers."
    assert add.calls == [((2, 3), {})]      # type: ignore[attr-defined]

    @timed
    def compute(n: int) -> int:
        return n

    assert compute.__name__ == "compute"    # pas "wrapper"

    assert delete_all(User(1, is_admin=True)) == "deleted"
    try:
        delete_all(User(2, is_admin=False))
    except PermissionDenied:
        pass
    else:
        raise AssertionError("PermissionDenied attendue")


if __name__ == "__main__":
    _checks()
    print("chapitre 27 — corrigés OK")
