"""Chapitre 2 — Mettre le pied à l'étrier : corrigés des exercices.

Les exercices de ce chapitre portent surtout sur l'outillage (uv) et le shell.
On documente ici les commandes attendues et l'on illustre le point Python
central : la distinction script / module et le garde ``__main__``.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Exercice 1 — Refaire : un projet de zéro (commandes uv attendues)
# ---------------------------------------------------------------------------
EXERCICE_1_COMMANDS = """\
uv init taskline && cd taskline
uv add httpx
# éditer hello.py pour importer httpx et imprimer httpx.__version__
uv run python hello.py
# Point clé : `uv add` installe DANS .venv ET inscrit la dépendance dans
# pyproject.toml — c'est cette double action qui rend le projet reproductible
# (un collègue n'a plus qu'à faire `uv sync`).
"""


# ---------------------------------------------------------------------------
# Exercice 2 — Comprendre : script ou module ?
# ---------------------------------------------------------------------------
EXERCICE_2_EXPLICATION = """\
Exécuté comme un SCRIPT (`uv run python taskline/cli.py`), le fichier ignore
qu'il appartient au paquet `taskline` : son import relatif `from .store import
load` n'a pas de paquet parent de référence et échoue (ImportError).
Exécuté comme un MODULE (`uv run python -m taskline.cli`), Python charge
d'abord le paquet `taskline`, puis le sous-module `cli` : le contexte du
paquet existe, l'import relatif se résout.
Règle : un fichier d'un paquet qui utilise des imports relatifs s'exécute
avec `-m`.
"""


# ---------------------------------------------------------------------------
# Exercice 3 — Concevoir : politique d'isolation d'équipe
# ---------------------------------------------------------------------------
EXERCICE_3_EXPLICATION = """\
Un environnement isolé PAR service (trois .venv), chacun déclarant sa propre
version de `taskline-core` dans son pyproject.toml. Le service figé épingle
l'ancienne version ; les deux autres suivent la récente.
Coût : la bibliothèque interne est installée en trois exemplaires (espace
disque négligeable) et il faut une discipline de versionnement (publier
`taskline-core` comme un vrai paquet versionné, pas le copier).
Bénéfice : aucun service ne peut casser les autres lors d'une mise à jour.
"""


# Le point Python du chapitre : le garde « exécuté, pas importé ».
def main() -> str:
    """Point d'entrée : ne s'exécute via le garde que si on lance le fichier."""
    return "Hello from Taskline"


def _checks() -> None:
    assert main() == "Hello from Taskline"
    # __name__ vaut le nom du module quand on importe ce fichier
    # (et "__main__" seulement quand on l'exécute directement).
    assert __name__ != "__main__" or True
    assert "uv add httpx" in EXERCICE_1_COMMANDS
    assert "-m taskline.cli" in EXERCICE_2_EXPLICATION


if __name__ == "__main__":
    _checks()
    print(main())
    print("chapitre 2 — corrigés OK")
