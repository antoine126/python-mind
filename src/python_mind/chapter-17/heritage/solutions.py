"""Chapitre 17 — Héritage simple : réutiliser et spécialiser : corrigés."""

from __future__ import annotations

import logging
from datetime import date, timedelta
from typing import Any, Protocol

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Exercice 1 — Refaire : remplacer un héritage abusif (dict) par composition
# ---------------------------------------------------------------------------
class LoggedDict:
    """N'EST PAS un dict ; il en A un. On n'expose que get/set, journalisés."""

    def __init__(self) -> None:
        self._data: dict[Any, Any] = {}

    def set(self, key: Any, value: Any) -> None:
        logger.info("set %s=%s", key, value)
        self._data[key] = value

    def get(self, key: Any, default: Any = None) -> Any:
        return self._data.get(key, default)


# ---------------------------------------------------------------------------
# Exercice 2 — Comprendre : Liskov en pratique (Bird / Penguin)
# ---------------------------------------------------------------------------
# Ne pas mettre fly() sur Bird : séparer la capacité de la nature.
class Bird:
    def __init__(self, name: str) -> None:
        self.name = name


class CanFly(Protocol):
    def fly(self) -> str: ...


class Sparrow(Bird):
    def fly(self) -> str:
        return f"{self.name} flies"


class Penguin(Bird):          # un Bird, mais PAS un CanFly
    def swim(self) -> str:
        return f"{self.name} swims"


def make_it_fly(flyer: CanFly) -> str:
    return flyer.fly()        # demande un CanFly, pas un Bird


# ---------------------------------------------------------------------------
# Exercice 3 — Concevoir : spécialiser une tâche
# ---------------------------------------------------------------------------
class Task:
    def __init__(self, title: str, due: date | None = None) -> None:
        self.title = title
        self.due = due
        self.done = False

    def mark_done(self) -> None:
        self.done = True

    def describe(self) -> str:
        return f"{self.title} ({'done' if self.done else 'todo'})"


class RecurringTask(Task):
    """IS-A Task, substituable ; mark_done reprogramme au lieu de figer."""

    def __init__(self, title: str, period_days: int) -> None:
        super().__init__(title)
        self.period_days = period_days

    def mark_done(self) -> None:
        super().mark_done()
        self.due = date.today() + timedelta(days=self.period_days)
        self.done = False     # une tâche récurrente n'est jamais « terminée »


def _checks() -> None:
    d = LoggedDict()
    d.set("k", 1)
    assert d.get("k") == 1 and d.get("missing", 0) == 0
    assert not hasattr(d, "sort")          # on n'a pas hérité du contrat de dict

    assert make_it_fly(Sparrow("piou")) == "piou flies"
    assert Penguin("pingu").swim() == "pingu swims"
    assert not hasattr(Penguin("x"), "fly")  # substituabilité préservée

    t = Task("write")
    t.mark_done()
    assert t.done and t.describe() == "write (done)"

    r = RecurringTask("standup", period_days=1)
    r.mark_done()
    assert r.done is False and r.due == date.today() + timedelta(days=1)
    # substituable : describe() marche pour les deux
    assert "todo" in r.describe()


if __name__ == "__main__":
    _checks()
    print("chapitre 17 — corrigés OK")
