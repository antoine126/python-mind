"""Chapitre 16 — Méthodes spéciales (dunder) : corrigés."""

from __future__ import annotations

import functools


# ---------------------------------------------------------------------------
# Exercice 1 — Refaire : un repr et une égalité
# ---------------------------------------------------------------------------
class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Point(x={self.x}, y={self.y})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return NotImplemented
        return (self.x, self.y) == (other.x, other.y)

    def __hash__(self) -> int:                  # cohérent avec __eq__
        return hash((self.x, self.y))


# ---------------------------------------------------------------------------
# Exercice 2 — Comprendre : pourquoi il n'est plus hashable
# ---------------------------------------------------------------------------
# Redéfinir __eq__ met __hash__ à None ; il faut le restaurer explicitement.
class Tag:
    def __init__(self, name: str) -> None:
        self.name = name

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Tag):
            return NotImplemented
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)


# ---------------------------------------------------------------------------
# Exercice 3 — Concevoir : un type Money complet
# ---------------------------------------------------------------------------
@functools.total_ordering
class Money:
    def __init__(self, cents: int, currency: str = "EUR") -> None:
        self.cents = cents
        self.currency = currency

    def __repr__(self) -> str:                  # pour le développeur
        return f"Money(cents={self.cents}, currency={self.currency!r})"

    def __str__(self) -> str:                   # pour l'utilisateur
        return f"{self.cents / 100:.2f} {self.currency}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        return (self.cents, self.currency) == (other.cents, other.currency)

    def __hash__(self) -> int:
        return hash((self.cents, self.currency))

    def __lt__(self, other: "Money") -> bool:
        if self.currency != other.currency:
            raise ValueError("cannot compare different currencies")
        return self.cents < other.cents

    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("cannot add different currencies")
        # renvoie un NOUVEL objet (immuable), ne mute pas self
        return Money(self.cents + other.cents, self.currency)


def _checks() -> None:
    assert repr(Point(1, 2)) == "Point(x=1, y=2)"
    assert Point(1, 2) == Point(1, 2)
    assert {Point(1, 2)}                          # hashable

    assert len({Tag("a"), Tag("a"), Tag("b")}) == 2

    assert str(Money(1099)) == "10.99 EUR"
    assert Money(100) == Money(100)
    assert Money(100) < Money(200)                # via __lt__
    assert Money(100) <= Money(100)               # dérivé par total_ordering
    assert (Money(100) + Money(50)).cents == 150
    for bad in (
        lambda: Money(1, "EUR") + Money(1, "USD"),
        lambda: Money(1, "EUR") < Money(1, "USD"),
    ):
        try:
            bad()
        except ValueError:
            pass
        else:
            raise AssertionError("ValueError attendue (devises différentes)")


if __name__ == "__main__":
    _checks()
    print("chapitre 16 — corrigés OK")
