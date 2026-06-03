"""Chapitre 28 — Gestionnaires de contexte : corrigés."""

from __future__ import annotations

import threading
from contextlib import contextmanager
from collections.abc import Iterator


# ---------------------------------------------------------------------------
# Exercice 1 — Refaire : sécuriser une ressource (un verrou)
# ---------------------------------------------------------------------------
def update_shared_state(lock: threading.Lock, state: list[int]) -> None:
    """Le verrou est libéré quoi qu'il arrive, même si le corps lève."""
    with lock:
        state.append(1)


# ---------------------------------------------------------------------------
# Exercice 2 — Comprendre : l'exception avalée
# ---------------------------------------------------------------------------
class Conn:
    """__exit__ renvoie False : il libère la ressource SANS avaler l'erreur."""

    def __init__(self) -> None:
        self.opened = False
        self.closed = False

    def __enter__(self) -> "Conn":
        self.opened = True
        return self

    def __exit__(self, exc_type: object, exc_val: object, exc_tb: object) -> bool:
        self.closed = True            # toujours libérer
        return False                  # laisser l'exception se propager


# ---------------------------------------------------------------------------
# Exercice 3 — Concevoir : une transaction Taskline
# ---------------------------------------------------------------------------
class FakeDB:
    def __init__(self) -> None:
        self.log: list[str] = []

    def begin(self) -> None:
        self.log.append("begin")

    def commit(self) -> None:
        self.log.append("commit")

    def rollback(self) -> None:
        self.log.append("rollback")


@contextmanager
def transaction(db: FakeDB) -> Iterator[FakeDB]:
    """commit si succès, rollback puis re-raise si échec."""
    db.begin()
    try:
        yield db
        db.commit()                   # chemin de succès
    except Exception:
        db.rollback()                 # chemin d'échec
        raise                         # ne pas cacher l'erreur


def _checks() -> None:
    lock = threading.Lock()
    state: list[int] = []
    update_shared_state(lock, state)
    assert state == [1] and not lock.locked()

    conn = Conn()
    try:
        with conn:
            raise RuntimeError("boom")
    except RuntimeError:
        pass
    else:
        raise AssertionError("l'exception aurait dû se propager")
    assert conn.opened and conn.closed       # libérée malgré l'erreur

    db = FakeDB()
    with transaction(db):
        pass
    assert db.log == ["begin", "commit"]

    db2 = FakeDB()
    try:
        with transaction(db2):
            raise ValueError("fail")
    except ValueError:
        pass
    assert db2.log == ["begin", "rollback"]


if __name__ == "__main__":
    _checks()
    print("chapitre 28 — corrigés OK")
