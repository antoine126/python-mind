"""Chapitre 4 — Conditions et flot de contrôle : corrigés."""

from __future__ import annotations

from typing import Any


# ---------------------------------------------------------------------------
# Exercice 1 — Refaire : prédire la truthiness
# ---------------------------------------------------------------------------
def truthiness_table() -> dict[str, bool]:
    """Pour chaque valeur, dit si ``if v:`` entre dans le bloc."""
    valeurs: dict[str, Any] = {
        "0": 0,
        '"0"': "0",
        "[]": [],
        "[0]": [0],
        "None": None,
        '" "': " ",
        "0.0": 0.0,
        "{}": {},
    }
    return {label: bool(v) for label, v in valeurs.items()}


# ---------------------------------------------------------------------------
# Exercice 2 — Comprendre : aplatir (clauses de garde)
# ---------------------------------------------------------------------------
class Order:
    def __init__(self, items: list[str], total: float) -> None:
        self.items = items
        self.total = total


def shipping_cost(order: Order | None) -> int | None:
    """Mêmes règles, mais aplaties par des clauses de garde + un ternaire."""
    if order is None or not order.items:
        return None
    return 5 if order.total < 50 else 0


# ---------------------------------------------------------------------------
# Exercice 3 — Concevoir : aiguiller des événements (dict de handlers)
# ---------------------------------------------------------------------------
def _on_added(e: dict) -> str:
    return f"new task: {e['title']}"


def _on_done(e: dict) -> str:
    return f"task {e['id']} completed"


# Ajouter un type = ajouter une entrée, sans toucher au reste (ouvert/fermé).
HANDLERS = {"task_added": _on_added, "task_done": _on_done}


def handle_event(event: dict) -> str:
    handler = HANDLERS.get(event["type"])
    if handler is None:                 # gérer la clé manquante explicitement
        return "unknown event"
    return handler(event)


def _checks() -> None:
    table = truthiness_table()
    assert table == {
        "0": False, '"0"': True, "[]": False, "[0]": True,
        "None": False, '" "': True, "0.0": False, "{}": False,
    }

    assert shipping_cost(None) is None
    assert shipping_cost(Order([], 10)) is None
    assert shipping_cost(Order(["a"], 30)) == 5
    assert shipping_cost(Order(["a"], 80)) == 0

    assert handle_event({"type": "task_added", "title": "write"}) == "new task: write"
    assert handle_event({"type": "task_done", "id": 7}) == "task 7 completed"
    assert handle_event({"type": "unknown"}) == "unknown event"


if __name__ == "__main__":
    _checks()
    print("chapitre 4 — corrigés OK")
