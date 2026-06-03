"""Chapitre 38 — Principes de conception : SOLID, couplage, cohésion : corrigés."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


# ---------------------------------------------------------------------------
# Exercice 1 — Refaire : découper l'objet-dieu (responsabilité unique, S)
# ---------------------------------------------------------------------------
@dataclass
class User:
    name: str
    email: str


class UserValidator:           # change si les règles de validation changent
    def validate(self, user: User) -> bool:
        return "@" in user.email and bool(user.name)


class UserRepository:          # change si la persistance change
    def __init__(self) -> None:
        self._saved: list[User] = []

    def save(self, user: User) -> None:
        self._saved.append(user)


class WelcomeMailer:           # change si la politique d'e-mail change
    def __init__(self) -> None:
        self.sent: list[str] = []

    def send(self, user: User) -> None:
        self.sent.append(user.email)


# ---------------------------------------------------------------------------
# Exercice 2 — Comprendre : couplage (inversion de dépendances, D)
# ---------------------------------------------------------------------------
class Database(Protocol):
    def insert(self, row: dict) -> None: ...


class Service:
    """Dépend d'une ABSTRACTION (Protocol), pas d'un Postgres concret :
    testable avec un faux, remplaçable sans modifier Service."""

    def __init__(self, db: Database) -> None:
        self.db = db          # injecté

    def create(self, name: str) -> None:
        self.db.insert({"name": name})


# ---------------------------------------------------------------------------
# Exercice 3 — Concevoir : étendre Taskline sans le casser (ouvert/fermé, O)
# ---------------------------------------------------------------------------
@dataclass
class Task:
    title: str


class Exporter(Protocol):
    def export(self, tasks: list[Task]) -> bytes: ...


class CsvExporter:
    def export(self, tasks: list[Task]) -> bytes:
        return ("\n".join(t.title for t in tasks)).encode()


class JsonExporter:
    def export(self, tasks: list[Task]) -> bytes:
        import json
        return json.dumps([t.title for t in tasks]).encode()


class PdfExporter:             # AJOUT : zéro changement à export_tasks
    def export(self, tasks: list[Task]) -> bytes:
        return b"%PDF-1.4 " + b", ".join(t.title.encode() for t in tasks)


def export_tasks(tasks: list[Task], exporter: Exporter) -> bytes:
    """Fermé à la modification, ouvert à l'extension : dépend de l'abstraction."""
    return exporter.export(tasks)


def _checks() -> None:
    user = User("ada", "ada@example.com")
    assert UserValidator().validate(user)
    repo = UserRepository()
    repo.save(user)
    mailer = WelcomeMailer()
    mailer.send(user)
    assert repo._saved == [user] and mailer.sent == ["ada@example.com"]

    inserted: list[dict] = []

    class FakeDB:
        def insert(self, row: dict) -> None:
            inserted.append(row)

    Service(FakeDB()).create("write")
    assert inserted == [{"name": "write"}]

    tasks = [Task("a"), Task("b")]
    assert export_tasks(tasks, CsvExporter()) == b"a\nb"
    assert export_tasks(tasks, JsonExporter()) == b'["a", "b"]'
    assert export_tasks(tasks, PdfExporter()).startswith(b"%PDF")


if __name__ == "__main__":
    _checks()
    print("chapitre 38 — corrigés OK")
