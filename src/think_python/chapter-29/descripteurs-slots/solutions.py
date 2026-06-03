"""Chapitre 29 — Descripteurs et __slots__ : corrigés."""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Exercice 1 — Refaire : property ou descripteur (besoin unique -> property)
# ---------------------------------------------------------------------------
class Measurement:
    """Logique d'accès utilisée une seule fois : @property suffit."""

    def __init__(self, temperature: float) -> None:
        self.temperature = temperature   # passe par le setter

    @property
    def temperature(self) -> float:
        return self._temperature

    @temperature.setter
    def temperature(self, value: float) -> None:
        if value < -273:
            raise ValueError("below absolute zero")
        self._temperature = value


# ---------------------------------------------------------------------------
# Exercice 2 — Comprendre : la valeur partagée (ranger sur l'instance)
# ---------------------------------------------------------------------------
class Field:
    def __set_name__(self, owner: type, name: str) -> None:
        self._name = f"_{name}"

    def __get__(self, obj: object, objtype: type | None = None) -> object:
        if obj is None:
            return self
        return getattr(obj, self._name)

    def __set__(self, obj: object, value: object) -> None:
        setattr(obj, self._name, value)   # rangé PAR instance


# ---------------------------------------------------------------------------
# Exercice 3 — Concevoir : des champs validés réutilisables (descripteur)
# ---------------------------------------------------------------------------
class BoundedInt:
    """Un « gardien partagé » : la même règle réutilisée sur plusieurs classes."""

    def __init__(self, lo: int, hi: int) -> None:
        self.lo, self.hi = lo, hi

    def __set_name__(self, owner: type, name: str) -> None:
        self._name = f"_{name}"

    def __get__(self, obj: object, objtype: type | None = None) -> object:
        if obj is None:
            return self
        return getattr(obj, self._name)

    def __set__(self, obj: object, value: int) -> None:
        if not self.lo <= value <= self.hi:
            raise ValueError(f"must be in [{self.lo}, {self.hi}]")
        setattr(obj, self._name, value)


class Task:
    priority = BoundedInt(1, 5)
    progress = BoundedInt(0, 100)

    def __init__(self, priority: int, progress: int) -> None:
        self.priority = priority
        self.progress = progress


class Order:
    quantity = BoundedInt(0, 10_000)

    def __init__(self, quantity: int) -> None:
        self.quantity = quantity


def _checks() -> None:
    m = Measurement(20.0)
    assert m.temperature == 20.0
    try:
        Measurement(-300)
    except ValueError:
        pass
    else:
        raise AssertionError("ValueError attendue (sous le zéro absolu)")

    # __set_name__ + setattr : chaque instance a SA valeur (pas de partage).
    class Holder:
        x = Field()

        def __init__(self, x: object) -> None:
            self.x = x

    a, b = Holder(1), Holder(2)
    assert a.x == 1 and b.x == 2

    t = Task(priority=3, progress=50)
    assert t.priority == 3 and t.progress == 50
    o = Order(quantity=100)
    assert o.quantity == 100
    for bad in (lambda: Task(0, 50), lambda: Order(99_999_999)):
        try:
            bad()
        except ValueError:
            pass
        else:
            raise AssertionError("ValueError attendue (borne dépassée)")


if __name__ == "__main__":
    _checks()
    print("chapitre 29 — corrigés OK")
