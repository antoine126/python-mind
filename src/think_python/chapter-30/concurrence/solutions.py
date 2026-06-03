"""Chapitre 30 — Concurrence : le bon modèle pour le bon problème : corrigés."""

from __future__ import annotations

import asyncio
from collections.abc import Callable


# ---------------------------------------------------------------------------
# Exercice 1 — Refaire : choisir le modèle
# ---------------------------------------------------------------------------
def choose_model(task: str) -> str:
    """I/O-bound -> async/threads ; CPU-bound -> multiprocessing."""
    cpu_bound = {"resize_images", "compute_primes", "hash_blocks"}
    return "multiprocessing" if task in cpu_bound else "asyncio/threads"


EXERCICE_1 = {
    "a) télécharger 1000 pages web": "asyncio/threads (I/O)",
    "b) redimensionner 1000 images": "multiprocessing (CPU)",
    "c) 50 requêtes base de données": "threads/async (I/O)",
    "d) premiers jusqu'à 1e9": "multiprocessing (CPU)",
}


# ---------------------------------------------------------------------------
# Exercice 2 — Comprendre : pourquoi les threads n'accélèrent pas
# ---------------------------------------------------------------------------
EXERCICE_2 = """\
Le hachage est CPU-bound : il exécute du bytecode en continu. À cause du GIL,
un seul thread exécute du Python à la fois ; huit threads se relaient sur un
cœur sans paralléliser, et le coût de bascule peut même ralentir. Correction :
ProcessPoolExecutor (plusieurs processus, plusieurs cœurs, chacun son GIL) :

    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor() as pool:
        digests = list(pool.map(hash_block, blocks))
"""


# ---------------------------------------------------------------------------
# Exercice 3 — Concevoir : un agrégateur pour Taskline
# ---------------------------------------------------------------------------
async def _call(value: int) -> int:
    """Simule un appel réseau (I/O) : on « attend » puis on renvoie."""
    await asyncio.sleep(0)            # rend la main à la boucle d'événements
    return value


def score(a: int, b: int, c: int) -> int:
    """Calcul léger : reste en ligne (pas de processus pour si peu)."""
    return a + b + c


async def aggregate() -> int:
    """Les trois appels I/O se CHEVAUCHENT via gather ; le score reste inline."""
    a, b, c = await asyncio.gather(_call(1), _call(2), _call(3))
    return score(a, b, c)


def _checks() -> None:
    assert choose_model("resize_images") == "multiprocessing"
    assert choose_model("download_pages") == "asyncio/threads"
    assert len(EXERCICE_1) == 4

    assert asyncio.run(aggregate()) == 6      # 1 + 2 + 3


if __name__ == "__main__":
    _checks()
    print("chapitre 30 — corrigés OK")
