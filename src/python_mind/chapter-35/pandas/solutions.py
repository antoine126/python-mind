"""Chapitre 35 — Pandas : le couteau suisse des données tabulaires : corrigés.

Nécessite l'extra « data » : ``uv sync --extra data``.
"""

from __future__ import annotations

import pandas as pd


# ---------------------------------------------------------------------------
# Exercice 1 — Refaire : vectoriser une colonne
# ---------------------------------------------------------------------------
def add_tax(df: pd.DataFrame) -> pd.DataFrame:
    """Opération de colonne vectorisée, pas `apply` ligne à ligne."""
    df = df.copy()
    df["with_tax"] = df["price"] * 1.2
    return df


# ---------------------------------------------------------------------------
# Exercice 2 — Comprendre : vue ou copie
# ---------------------------------------------------------------------------
def clamp_negative_scores(df: pd.DataFrame) -> pd.DataFrame:
    """Un SEUL indexeur .loc pour modifier les cellules sélectionnées
    (le double crochet chaîné agirait sur une copie : SettingWithCopyWarning)."""
    df = df.copy()
    df.loc[df["score"] < 0, "score"] = 0
    return df


# ---------------------------------------------------------------------------
# Exercice 3 — Concevoir : un rapport de ventes
# ---------------------------------------------------------------------------
def sales_report(df: pd.DataFrame) -> pd.DataFrame:
    """Total des ventes par région et par mois (groupby vectorisé).

    On supprime les montants manquants (un montant inconnu n'est pas zéro —
    le compter comme 0 sous-estimerait le total ; choix métier documenté).
    """
    df = df.dropna(subset=["amount"])
    return (
        df.groupby(["region", "month"])["amount"].sum().reset_index()
    )


def _checks() -> None:
    df = pd.DataFrame({"price": [10.0, 20.0]})
    assert list(add_tax(df)["with_tax"]) == [12.0, 24.0]

    scores = pd.DataFrame({"score": [-1, 2, -3, 4]})
    assert list(clamp_negative_scores(scores)["score"]) == [0, 2, 0, 4]

    sales = pd.DataFrame(
        {
            "region": ["N", "N", "S", "N"],
            "month": ["jan", "jan", "jan", "feb"],
            "amount": [10.0, 20.0, 5.0, None],
        }
    )
    report = sales_report(sales)
    n_jan = report[(report["region"] == "N") & (report["month"] == "jan")]
    assert int(n_jan["amount"].iloc[0]) == 30      # 10 + 20, NaN ignoré


if __name__ == "__main__":
    _checks()
    print("chapitre 35 — corrigés OK")
