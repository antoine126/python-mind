"""Chapitre 18 — Héritage multiple et MRO : corrigés."""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Exercice 1 — Refaire : prédire le MRO et la sortie
# ---------------------------------------------------------------------------
class A:
    def greet(self) -> list[str]:
        return ["A"]


class B(A):
    def greet(self) -> list[str]:
        return ["B"] + super().greet()


class C(A):
    def greet(self) -> list[str]:
        return ["C"] + super().greet()


class D(C, B):                       # C avant B : MRO [D, C, B, A, object]
    def greet(self) -> list[str]:
        return ["D"] + super().greet()


def mro_names(cls: type) -> list[str]:
    return [c.__name__ for c in cls.__mro__]


# ---------------------------------------------------------------------------
# Exercice 2 — Comprendre : la chaîne qui casse (init coopératif)
# ---------------------------------------------------------------------------
# Le bug : Drawable non coopératif lève TypeError dès qu'un kwarg le traverse
# (Button(color="red")). Correctif : le rendre coopératif.
class Base:
    def __init__(self, **kwargs: object) -> None:
        super().__init__(**kwargs)   # termine la chaîne à object


class Clickable(Base):
    def __init__(self, *, on_click: object = None, **kwargs: object) -> None:
        super().__init__(**kwargs)
        self.on_click = on_click


class Drawable(Base):
    def __init__(self, *, color: str = "black", **kwargs: object) -> None:
        super().__init__(**kwargs)   # accepte ET transmet le reste
        self.color = color           # consomme son propre kwarg


class Button(Clickable, Drawable):
    def __init__(self, *, label: str, **kwargs: object) -> None:
        super().__init__(**kwargs)   # parcourt tout le MRO une fois
        self.label = label


# ---------------------------------------------------------------------------
# Exercice 3 — Concevoir : capacités d'un widget (mixin léger + composition)
# ---------------------------------------------------------------------------
class LoggableMixin:                 # capacité légère, sans état, transversale
    def log(self, msg: str) -> None:
        logger.info("%s: %s", type(self).__name__, msg)


class Renderer:
    def render(self, label: str) -> str:
        return f"[{label}]"


class Widget(LoggableMixin):         # mixin pour le léger
    def __init__(self, label: str, renderer: Renderer) -> None:
        self.label = label
        self.renderer = renderer     # composition pour la partie « lourde »

    def draw(self) -> str:
        return self.renderer.render(self.label)


def _checks() -> None:
    assert mro_names(D) == ["D", "C", "B", "A", "object"]
    assert D().greet() == ["D", "C", "B", "A"]

    b = Button(label="OK", on_click="save", color="blue")
    assert (b.label, b.on_click, b.color) == ("OK", "save", "blue")
    # Avant correction, Button(color=...) levait TypeError ; ici tout passe.
    assert Button(label="x").color == "black"

    w = Widget("OK", Renderer())
    assert w.draw() == "[OK]"
    w.log("clicked")                 # capacité greffée par le mixin


if __name__ == "__main__":
    _checks()
    print("chapitre 18 — corrigés OK")
