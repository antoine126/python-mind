"""Chapitre 12 — exemple de vrais tests pytest (illustration du chapitre).

Pour les lancer isolément : ``uv run pytest chapter-12/tester/test_billing.py``
(le reste du dépôt est vérifié par ``tests/test_solutions.py``).
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))
from solutions import Task, TaskStore, with_tax  # noqa: E402


@pytest.fixture
def store() -> TaskStore:
    """Un contexte NEUF par test (isolation)."""
    s = TaskStore()
    s.add(Task("write"))
    s.add(Task("test"))
    return s


def test_count(store: TaskStore) -> None:
    assert store.count() == 2


def test_added_task_is_retrievable() -> None:
    # Arrange / Act / Assert — par l'interface publique.
    store = TaskStore()
    task = store.add(Task("write"))
    assert store.get(task.id).title == "write"


@pytest.mark.parametrize(
    "amount, rate, expected",
    [(100, 0.2, 120), (0, 0.2, 0), (100, 0.0, 100), (100, 1.0, 200)],
)
def test_with_tax_valid(amount: int, rate: float, expected: float) -> None:
    assert with_tax(amount, rate) == expected


def test_with_tax_rejects_negative_rate() -> None:
    with pytest.raises(ValueError):
        with_tax(100, rate=-0.1)
