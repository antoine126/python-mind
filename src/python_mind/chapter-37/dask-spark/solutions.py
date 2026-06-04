"""Chapitre 37 — Quand une seule machine ne suffit plus : Dask et PySpark.

Exercices de décision (volume + infrastructure -> outil) : stdlib, testables.
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Exercice 1 — Refaire : choisir l'outil (volume + machine)
# ---------------------------------------------------------------------------
def choose_tool(size_gb: float, ram_gb: float, distributed_infra: bool) -> str:
    """On monte d'un cran SEULEMENT quand le précédent ne suffit plus."""
    if size_gb <= ram_gb:
        return "pandas/polars"                      # tient en RAM
    if not distributed_infra:
        return "polars-streaming/dask"              # > RAM, une machine
    return "spark"                                  # > une machine, cluster


EXERCICE_1 = {
    "a) 0.5 Go sur un portable": "pandas/polars",
    "b) 200 Go sur 64 Go de RAM": "polars-streaming/dask",
    "c) 10 To sur cluster Hadoop": "spark",
    "d) groupby 50 Go, API façon pandas": "dask",
}


# ---------------------------------------------------------------------------
# Exercice 2 — Comprendre : pourquoi pas Spark
# ---------------------------------------------------------------------------
EXERCICE_2 = """\
1. LATENCE de démarrage : Spark lance une JVM, initialise une session,
   planifie un graphe distribué — plusieurs secondes AVANT le moindre calcul,
   là où Polars traite 50 000 lignes en millisecondes.
2. COORDINATION/COMPLEXITÉ : Spark partitionne, sérialise, communique entre
   exécuteurs (shuffle) — du travail inutile sur un si petit jeu — et impose
   une infrastructure distribuée. « Scalable » n'est pas « rapide » : à petite
   échelle, le distribué est un handicap.
"""


# ---------------------------------------------------------------------------
# Exercice 3 — Concevoir : faire grandir le pipeline de Taskline
# ---------------------------------------------------------------------------
TRAJECTOIRE = [
    ("1 Go", "pandas / polars eager (tient en RAM)"),
    ("dizaines de Go", "polars lazy (pushdowns, parallélisme)"),
    ("centaines de Go > RAM, 1 machine", "polars streaming / dask"),
    ("To, plusieurs machines", "pyspark — seulement si l'infra existe"),
]

A_VERIFIER_AVANT_CHAQUE_MONTEE = """\
Profiler (le goulot est-il vraiment le volume ?), optimiser l'étape actuelle
(colonnes utiles, types compacts, lazy) avant de changer d'outil, et estimer
le coût (infra, complexité, apprentissage) face au gain. On ne distribue
jamais « par anticipation » : on monte d'un cran quand — et seulement quand —
le cran actuel sature, mesure à l'appui.
"""


def _checks() -> None:
    assert choose_tool(0.5, 16, distributed_infra=False) == "pandas/polars"
    assert choose_tool(200, 64, distributed_infra=False) == "polars-streaming/dask"
    assert choose_tool(10_000, 64, distributed_infra=True) == "spark"
    assert len(TRAJECTOIRE) == 4
    assert TRAJECTOIRE[0][1].startswith("pandas")
    assert TRAJECTOIRE[-1][1].startswith("pyspark")


if __name__ == "__main__":
    _checks()
    print("chapitre 37 — corrigés OK")
