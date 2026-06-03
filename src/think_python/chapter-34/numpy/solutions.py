"""Chapitre 34 — NumPy : penser en tableaux : corrigés.

Nécessite l'extra « data » : ``uv sync --extra data``.
"""

from __future__ import annotations

import numpy as np


# ---------------------------------------------------------------------------
# Exercice 1 — Refaire : vectoriser
# ---------------------------------------------------------------------------
def even_squares_or_zero(data: np.ndarray) -> np.ndarray:
    """`np.where` est le « ternaire vectorisé » : condition appliquée à tout
    le tableau, sans boucle Python."""
    return np.where(data > 0, data * data, 0)


# ---------------------------------------------------------------------------
# Exercice 2 — Comprendre : le broadcasting
# ---------------------------------------------------------------------------
def apply_discount(prices: np.ndarray, discount: np.ndarray) -> np.ndarray:
    """`discount` (forme (3,)) est broadcasté sur les lignes de `prices`
    (forme (n, 3)) : une remise par magasin appliquée à tous les produits."""
    return prices * (1 - discount)


# ---------------------------------------------------------------------------
# Exercice 3 — Concevoir : normaliser des mesures
# ---------------------------------------------------------------------------
def normalize(x: np.ndarray) -> np.ndarray:
    """axis=0 -> statistiques PAR colonne ; broadcasting sur les lignes."""
    mean = x.mean(axis=0)
    std = x.std(axis=0)
    return (x - mean) / std


def _checks() -> None:
    a = np.array([-2, 3, 0, 4])
    assert np.array_equal(even_squares_or_zero(a), np.array([0, 9, 0, 16]))

    prices = np.array([[10.0, 20.0, 30.0], [40.0, 50.0, 60.0]])
    discount = np.array([0.0, 0.5, 1.0])
    net = apply_discount(prices, discount)
    assert net.shape == (2, 3)
    assert np.allclose(net, [[10, 10, 0], [40, 25, 0]])

    x = np.array([[1.0, 10.0], [3.0, 30.0]])
    z = normalize(x)
    assert np.allclose(z.mean(axis=0), [0.0, 0.0], atol=1e-9)
    assert np.allclose(z.std(axis=0), [1.0, 1.0], atol=1e-9)


if __name__ == "__main__":
    _checks()
    print("chapitre 34 — corrigés OK")
