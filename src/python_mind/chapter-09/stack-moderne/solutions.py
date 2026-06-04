"""Chapitre 9 — La stack moderne (uv, ruff, ty) : corrigés.

Exercices essentiellement outillage/CI : on documente les réponses et l'on
expose l'ordre recommandé des étapes de CI sous forme testable.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Exercice 1 — Refaire : initialiser une stack propre
# ---------------------------------------------------------------------------
EXERCICE_1_COMMANDS = """\
uv init taskline && cd taskline
uv add fastapi
uv add --dev pytest ruff
uv run ruff format .
uv run ruff check --fix .
uv run pytest
# Point clé : pytest et ruff vont dans le groupe `dev`, séparés des
# dépendances d'exécution (fastapi). L'image de prod n'embarque pas les
# outils de test.
"""

# ---------------------------------------------------------------------------
# Exercice 2 — Comprendre : pourquoi le lockfile
# ---------------------------------------------------------------------------
EXERCICE_2 = """\
pyproject.toml dit l'INTENTION (`fastapi>=0.110`). Sans lockfile, deux
machines installées à deux dates obtiennent des versions différentes de
fastapi (et de ses dépendances transitives comme starlette) : « ça marche
chez moi » peut casser ailleurs, sans qu'aucun fichier ne le montre.
uv.lock fige l'arbre COMPLET des versions ; `uv sync` reconstruit
exactement le même environnement partout. Le lockfile dit le FAIT.
"""

# ---------------------------------------------------------------------------
# Exercice 3 — Concevoir : choisir le type checker
# ---------------------------------------------------------------------------
EXERCICE_3 = {
    "api_fastapi_neuve": "ty (vitesse, cohérence Astral, pas de plugin) en "
    "assumant la bêta — ou mypy si la CI doit être stable dès le départ.",
    "django_historique": "mypy + plugin Django (ou pyrefly) : l'ORM exige des "
    "plugins que ty n'a pas.",
    "lib_scientifique": "ty convient (code typé pur) ; pyrefly/mypy restent "
    "des choix sûrs.",
}


# ---------------------------------------------------------------------------
# Exercice 4 — Concevoir : une CI de qualité (ordre = fail fast)
# ---------------------------------------------------------------------------
def ci_steps() -> list[str]:
    """Du moins coûteux au plus lourd : on rend l'info la moins chère d'abord."""
    return [
        "ruff format --check",   # quasi instantané
        "ruff check",            # rapide
        "ty check (ou mypy)",    # vérification de types
        "pytest",                # le plus long
    ]


def _checks() -> None:
    assert "uv add --dev pytest ruff" in EXERCICE_1_COMMANDS
    assert "uv.lock" in EXERCICE_2
    assert set(EXERCICE_3) == {
        "api_fastapi_neuve", "django_historique", "lib_scientifique"
    }
    steps = ci_steps()
    assert steps[0].startswith("ruff format")
    assert steps[-1] == "pytest"            # le plus lent en dernier


if __name__ == "__main__":
    _checks()
    print("chapitre 9 — corrigés OK")
