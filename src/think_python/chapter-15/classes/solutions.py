"""Chapitre 15 — Classes, attributs, méthodes, encapsulation : corrigés."""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Exercice 1 — Refaire : corriger l'état partagé
# ---------------------------------------------------------------------------
class Playlist:
    def __init__(self) -> None:
        self.songs: list[str] = []      # une liste PAR instance

    def add(self, song: str) -> None:
        self.songs.append(song)


# ---------------------------------------------------------------------------
# Exercice 2 — Comprendre : property ou attribut
# ---------------------------------------------------------------------------
class Rectangle:
    """width/height : attributs publics simples (données indépendantes).
    area/perimeter : @property (données DÉRIVÉES, toujours cohérentes)."""

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

    @property
    def area(self) -> int:
        return self.width * self.height

    @property
    def perimeter(self) -> int:
        return 2 * (self.width + self.height)


# ---------------------------------------------------------------------------
# Exercice 3 — Concevoir : un compte bancaire avec invariant
# ---------------------------------------------------------------------------
class Account:
    """Invariant « solde >= 0 » vérifié à CHAQUE porte d'entrée."""

    def __init__(self, owner: str, balance: int = 0) -> None:
        if balance < 0:
            raise ValueError("balance cannot be negative")
        self.owner = owner
        self._balance = balance         # caché : pas de setter direct

    @property
    def balance(self) -> int:           # lecture seule
        return self._balance

    def deposit(self, amount: int) -> None:
        if amount <= 0:
            raise ValueError("amount must be positive")
        self._balance += amount

    def withdraw(self, amount: int) -> None:
        if amount > self._balance:
            raise ValueError("insufficient funds")
        self._balance -= amount

    @classmethod
    def from_dict(cls, data: dict) -> "Account":
        return cls(data["owner"], data.get("balance", 0))


def _checks() -> None:
    a, b = Playlist(), Playlist()
    a.add("song")
    assert a.songs == ["song"] and b.songs == []   # pas de partage

    r = Rectangle(3, 4)
    assert r.area == 12 and r.perimeter == 14
    r.width = 5
    assert r.area == 20                              # dérivé, toujours cohérent

    acc = Account.from_dict({"owner": "ada", "balance": 100})
    acc.deposit(50)
    acc.withdraw(30)
    assert acc.balance == 120
    for bad in (lambda: acc.withdraw(10_000), lambda: Account("x", -1)):
        try:
            bad()
        except ValueError:
            pass
        else:
            raise AssertionError("ValueError attendue")


if __name__ == "__main__":
    _checks()
    print("chapitre 15 — corrigés OK")
