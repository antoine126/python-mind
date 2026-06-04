"""Chapitre 42 — Patterns comportementaux : corrigés."""

from __future__ import annotations

import weakref
from collections.abc import Callable


# ---------------------------------------------------------------------------
# Exercice 1 — Refaire : Strategy en fonction
# ---------------------------------------------------------------------------
class Item:
    def __init__(self, name: str, date_: int) -> None:
        self.name, self.date = name, date_


def by_name(items: list[Item]) -> list[Item]:
    return sorted(items, key=lambda x: x.name)


def by_date(items: list[Item]) -> list[Item]:
    return sorted(items, key=lambda x: x.date)


def arrange(items: list[Item], strategy: Callable[[list[Item]], list[Item]]):
    """La stratégie est une fonction passée en argument."""
    return strategy(items)


# ---------------------------------------------------------------------------
# Exercice 2 — Comprendre : la fuite d'observers
# ---------------------------------------------------------------------------
EXERCICE_2 = """\
Quand un objet s'abonne (board.subscribe(self.on_event)), le board garde une
référence vers son callback — donc vers l'objet. Si cet objet a une durée de
vie courte, il DEVRAIT être collecté quand on n'en a plus besoin ; mais le
board le retient (compteur de références non nul). Résultat : l'objet « mort »
reste en mémoire ET continue d'être notifié (comportement fantôme). Sans
unsubscribe (ou weakref), ces abonnés s'accumulent : fuite.
"""


class TaskBoard:
    """Variante sûre : références FAIBLES, abonnés collectés normalement."""

    def __init__(self) -> None:
        self._subs: list[weakref.ref] = []

    def subscribe(self, callback: Callable[[str], None]) -> None:
        self._subs.append(weakref.ref(callback))

    def add_task(self, title: str) -> int:
        delivered = 0
        for ref in self._subs:
            cb = ref()
            if cb is not None:          # l'abonné existe encore
                cb(title)
                delivered += 1
        return delivered


# ---------------------------------------------------------------------------
# Exercice 3 — Concevoir : un pipeline de validation (Chain of Responsibility)
# ---------------------------------------------------------------------------
class Task:
    def __init__(self, title: str, priority: int) -> None:
        self.title, self.priority = title, priority


def not_blank(task: Task) -> str | None:
    return None if task.title.strip() else "title is blank"


def valid_priority(task: Task) -> str | None:
    return None if 1 <= task.priority <= 5 else "bad priority"


def validate(task: Task, rules: list[Callable[[Task], str | None]]) -> list[str]:
    """Chaque règle accepte (None) ou rejette (un message) ; le moteur les
    parcourt. Ajouter une règle = l'ajouter à la liste (ouvert/fermé)."""
    return [msg for rule in rules if (msg := rule(task)) is not None]


RULES = [not_blank, valid_priority]


def _checks() -> None:
    items = [Item("b", 2), Item("a", 1)]
    assert [i.name for i in arrange(items, by_name)] == ["a", "b"]
    assert [i.name for i in arrange(items, by_date)] == ["a", "b"]

    board = TaskBoard()

    def on_event(title: str) -> None:
        seen.append(title)

    seen: list[str] = []
    board.subscribe(on_event)
    assert board.add_task("write") == 1
    assert seen == ["write"]

    assert validate(Task("write", 3), RULES) == []
    assert validate(Task("", 9), RULES) == ["title is blank", "bad priority"]


if __name__ == "__main__":
    _checks()
    print("chapitre 42 — corrigés OK")
