"""Chapitre 41 — Patterns structurels : corrigés."""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Exercice 1 — Refaire : une Facade
# ---------------------------------------------------------------------------
class _DB:
    def fetch(self, user: str) -> dict:
        return {"user": user, "rows": 3}


class _Renderer:
    def render(self, data: dict) -> str:
        return f"PDF<{data['user']}:{data['rows']}>"


class _Storage:
    def __init__(self) -> None:
        self.uploaded: list[str] = []

    def upload(self, pdf: str) -> str:
        self.uploaded.append(pdf)
        return f"https://x/{len(self.uploaded)}"


class _Mailer:
    def __init__(self) -> None:
        self.notified: list[tuple[str, str]] = []

    def notify(self, user: str, url: str) -> None:
        self.notified.append((user, url))


class ReportFacade:
    """Une porte simple devant un sous-système complexe : le client appelle
    UNE méthode au lieu d'orchestrer quatre objets."""

    def __init__(self, db: _DB, renderer: _Renderer, storage: _Storage,
                 mailer: _Mailer) -> None:
        self._db, self._renderer = db, renderer
        self._storage, self._mailer = storage, mailer

    def publish_report(self, user: str) -> str:
        data = self._db.fetch(user)
        pdf = self._renderer.render(data)
        url = self._storage.upload(pdf)
        self._mailer.notify(user, url)
        return url


# ---------------------------------------------------------------------------
# Exercice 2 — Comprendre : Adapter ou duck typing
# ---------------------------------------------------------------------------
EXERCICE_2 = """\
Aucun Adapter nécessaire : vous contrôlez les deux classes ET leurs méthodes
send sont déjà compatibles -> le duck typing suffit. Un Adapter ne se
justifie que pour brancher un code TIERS dont l'interface diffère et qu'on ne
peut pas modifier. Ici ce serait de la cérémonie inutile.
"""


# ---------------------------------------------------------------------------
# Exercice 3 — Concevoir : l'arbre des tâches de Taskline (Composite)
# ---------------------------------------------------------------------------
class Task:                          # feuille
    def __init__(self, title: str, hours: int) -> None:
        self.title, self.hours = title, hours

    def total_hours(self) -> int:
        return self.hours


class TaskGroup:                     # composite : tâches OU sous-groupes
    def __init__(self, name: str) -> None:
        self.name = name
        self.items: list[Task | TaskGroup] = []

    def add(self, item: Task | TaskGroup) -> None:
        self.items.append(item)

    def total_hours(self) -> int:
        return sum(item.total_hours() for item in self.items)   # récursif


def _checks() -> None:
    facade = ReportFacade(_DB(), _Renderer(), _Storage(), mailer := _Mailer())
    url = facade.publish_report("ada")
    assert url.startswith("https://x/") and mailer.notified[0][0] == "ada"

    project = TaskGroup("project")
    project.add(Task("a", 2))
    sub = TaskGroup("sub")
    sub.add(Task("b", 3))
    sub.add(Task("c", 4))
    project.add(sub)
    # feuille et nœud répondent à la MÊME interface total_hours()
    assert Task("x", 5).total_hours() == 5
    assert project.total_hours() == 2 + 3 + 4


if __name__ == "__main__":
    _checks()
    print("chapitre 41 — corrigés OK")
