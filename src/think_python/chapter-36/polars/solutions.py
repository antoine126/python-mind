"""Chapitre 36 — Polars : la relève moderne : corrigés.

Nécessite l'extra « data » : ``uv sync --extra data``.
"""

from __future__ import annotations

import polars as pl


# ---------------------------------------------------------------------------
# Exercice 1 — Refaire : du Pandas au Polars (style « expressions »)
# ---------------------------------------------------------------------------
def net_by_region(df: pl.DataFrame) -> pl.DataFrame:
    return (
        df.filter(pl.col("amount") > 0)
        .with_columns((pl.col("amount") * 0.8).alias("net"))
        .group_by("region")
        .agg(pl.col("net").sum())
        .sort("region")
    )


# ---------------------------------------------------------------------------
# Exercice 2 — Comprendre : eager ou lazy
# ---------------------------------------------------------------------------
EXERCICE_2 = """\
En lazy, l'optimiseur applique le projection pushdown (ne lire que les
colonnes utilisées en bout de chaîne — 3 sur 50) et le predicate pushdown
(filtrer au plus tôt, idéalement pendant la lecture — ne garder que 1 % des
lignes). On évite de charger 47 colonnes inutiles ET 99 % des lignes.
En eager, chaque étape ignore les suivantes : on lirait tout, puis on
filtrerait — gaspillage.
"""


# ---------------------------------------------------------------------------
# Exercice 3 — Concevoir : un pipeline de reporting performant (lazy)
# ---------------------------------------------------------------------------
def sales_report_lazy(lf: pl.LazyFrame) -> pl.DataFrame:
    """scan/lazy -> select (projection) -> drop_nulls -> group_by -> collect.

    L'optimiseur réorganise le plan ; Polars exécute en parallèle sur tous
    les cœurs (pas de GIL).
    """
    return (
        lf.select(["region", "month", "amount"])
        .drop_nulls("amount")
        .group_by(["region", "month"])
        .agg(pl.col("amount").sum().alias("total"))
        .sort(["region", "month"])
        .collect()
    )


def _checks() -> None:
    df = pl.DataFrame(
        {"region": ["N", "N", "S"], "amount": [10.0, -5.0, 20.0]}
    )
    out = net_by_region(df)
    rows = {r["region"]: r["net"] for r in out.to_dicts()}
    assert rows["N"] == 8.0          # 10 * 0.8 (la ligne -5 est filtrée)
    assert rows["S"] == 16.0

    lf = pl.LazyFrame(
        {
            "region": ["N", "N", "S"],
            "month": ["jan", "jan", "jan"],
            "amount": [10.0, 20.0, None],
            "extra": [1, 2, 3],          # colonne non sélectionnée
        }
    )
    report = sales_report_lazy(lf)
    n = report.filter(
        (pl.col("region") == "N") & (pl.col("month") == "jan")
    )
    assert n["total"][0] == 30.0         # 10 + 20, None ignoré


if __name__ == "__main__":
    _checks()
    print("chapitre 36 — corrigés OK")
