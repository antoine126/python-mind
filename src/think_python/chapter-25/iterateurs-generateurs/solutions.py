"""Chapitre 25 — Itérateurs, générateurs et évaluation paresseuse : corrigés."""

from __future__ import annotations

from collections.abc import Iterable, Iterator


# ---------------------------------------------------------------------------
# Exercice 1 — Refaire : rendre paresseux
# ---------------------------------------------------------------------------
def even_squares(n: int) -> Iterator[int]:
    """Générateur : aucune liste matérialisée."""
    for i in range(n):
        if i % 2 == 0:
            yield i * i


# ---------------------------------------------------------------------------
# Exercice 2 — Comprendre : le générateur vide
# ---------------------------------------------------------------------------
def sum_twice_materialized(values: range) -> tuple[int, int]:
    """(a) Matérialiser une fois, itérer la liste deux fois."""
    nums = list(values)
    return sum(nums), sum(nums)


def sum_twice_recreated() -> tuple[int, int]:
    """(b) Recréer le générateur à chaque usage."""
    return sum(i for i in range(5)), sum(i for i in range(5))


# ---------------------------------------------------------------------------
# Exercice 3 — Concevoir : un pipeline de traitement (mémoire constante)
# ---------------------------------------------------------------------------
def non_empty(lines: Iterable[str]) -> Iterator[str]:
    for line in lines:
        if line:
            yield line


def parse(lines: Iterable[str]) -> Iterator[dict]:
    for line in lines:
        kind, _, rest = line.partition(":")
        yield {"type": kind, "payload": rest}


def only_done(events: Iterable[dict]) -> Iterator[dict]:
    for e in events:
        if e["type"] == "task_done":
            yield e


def count_done(lines: Iterable[str]) -> int:
    """Chaque ligne traverse tout le pipeline puis est jetée : mémoire O(1)."""
    pipeline = only_done(parse(non_empty(lines)))
    return sum(1 for _ in pipeline)


def _checks() -> None:
    assert list(even_squares(10)) == [0, 4, 16, 36, 64]
    assert sum(even_squares(10_000)) > 0          # fonctionne en flux

    # Générateur épuisé après un parcours.
    gen = (i for i in range(3))
    assert list(gen) == [0, 1, 2]
    assert list(gen) == []
    assert sum_twice_materialized(range(5)) == (10, 10)
    assert sum_twice_recreated() == (10, 10)

    lines = ["task_added:write", "", "task_done:1", "task_done:2", "noise"]
    assert count_done(lines) == 2


if __name__ == "__main__":
    _checks()
    print("chapitre 25 — corrigés OK")
