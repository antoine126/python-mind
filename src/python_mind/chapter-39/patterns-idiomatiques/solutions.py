"""Chapitre 39 — Les patterns idiomatiques Python : corrigés."""

from __future__ import annotations

from collections.abc import Callable, Iterator


# ---------------------------------------------------------------------------
# Exercice 1 — Refaire : dégonfler un Strategy (en fonction)
# ---------------------------------------------------------------------------
def no_discount(price: float) -> float:
    return price


def half_price(price: float) -> float:
    return price * 0.5


def checkout(price: float, discount: Callable[[float], float]) -> float:
    """La stratégie EST une fonction de première classe : ajouter une remise =
    écrire une fonction."""
    return discount(price)


# ---------------------------------------------------------------------------
# Exercice 2 — Comprendre : Iterator natif
# ---------------------------------------------------------------------------
class Node:
    def __init__(self, value: int, children: list["Node"] | None = None) -> None:
        self.value = value
        self.children = children or []


def walk_tree(node: Node) -> Iterator[int]:
    """Un générateur EST le pattern Iterator : Python fournit __iter__/__next__
    et gère l'état suspendu — aucune classe à écrire."""
    yield node.value
    for child in node.children:
        yield from walk_tree(child)


# ---------------------------------------------------------------------------
# Exercice 3 — Concevoir : un registre d'exporteurs (module + décorateur + dict)
# ---------------------------------------------------------------------------
_exporters: dict[str, Callable[[list[str]], bytes]] = {}


def register(name: str) -> Callable[[Callable], Callable]:
    def deco(fn: Callable) -> Callable:
        _exporters[name] = fn       # enregistrement déclaratif
        return fn

    return deco


def get_exporter(name: str) -> Callable[[list[str]], bytes]:
    return _exporters[name]


@register("csv")
def export_csv(titles: list[str]) -> bytes:
    return "\n".join(titles).encode()


@register("json")
def export_json(titles: list[str]) -> bytes:
    import json
    return json.dumps(titles).encode()


@register("pdf")                    # ajout : code du registre intact
def export_pdf(titles: list[str]) -> bytes:
    return b"%PDF " + ", ".join(titles).encode()


def _checks() -> None:
    assert checkout(100, no_discount) == 100
    assert checkout(100, half_price) == 50

    tree = Node(1, [Node(2, [Node(4)]), Node(3)])
    assert list(walk_tree(tree)) == [1, 2, 4, 3]

    assert get_exporter("csv")(["a", "b"]) == b"a\nb"
    assert get_exporter("json")(["a"]) == b'["a"]'
    assert get_exporter("pdf")(["a"]).startswith(b"%PDF")


if __name__ == "__main__":
    _checks()
    print("chapitre 39 — corrigés OK")
