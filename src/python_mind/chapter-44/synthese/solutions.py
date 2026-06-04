"""Chapitre 44 — Synthèse : reconnaître le problème avant le pattern : corrigés."""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Exercice 1 — Refaire : du symptôme au remède (réponse minimale pythonique)
# ---------------------------------------------------------------------------
def remedy(symptom: str) -> str:
    """Partir du symptôme vers la construction NATIVE minimale."""
    return {
        "algo_varie": "une fonction (Strategy)",
        "type_concret_varie": "fabrique / registre",
        "regle_dupliquee": "factoriser (DRY, règle de trois)",
        "couplage_fort": "abstraction + injection",
        "parcourir_structure": "un générateur (Iterator)",
    }[symptom]


EXERCICE_1 = {
    "a) cinq if qui choisissent un tri": "une fonction (Strategy)",
    "b) même connexion DB dans dix classes": "injection (composition root)",
    "c) règle de TVA copiée 3 fois": "factoriser en une fonction (DRY)",
    "d) parcourir un arbre sans exposer la structure": "un générateur",
}


# ---------------------------------------------------------------------------
# Exercice 2 — Comprendre : refuser un pattern
# ---------------------------------------------------------------------------
EXERCICE_2 = """\
Avec UN seul cas, Abstract Factory + Strategy + Observer sont de l'abstraction
PRÉMATURÉE : des couches/interfaces/magie pour une flexibilité dont rien ne
prouve qu'on aura besoin (YAGNI). Coût immédiat (lisibilité, maintenance),
bénéfice hypothétique.
Quand les introduire : à la RÈGLE DE TROIS — quand un 2e puis 3e cas réel
apparaissent et que le motif de variation est clair. Signal concret : « je
viens de copier-coller en changeant une ligne, pour la troisième fois ».
"""


# ---------------------------------------------------------------------------
# Exercice 3 — Concevoir : la revue d'architecture
# ---------------------------------------------------------------------------
REVUE = {
    "config par Singleton global": {
        "anti_pattern": "dépendance cachée",
        "remede_minimal": "injecter Settings par constructeur",
    },
    "DB + métier mélangés": {
        "anti_pattern": "responsabilité multiple (S)",
        "remede_minimal": "séparer Repository (données) et Service (métier)",
    },
    "export par if rouvert à chaque ajout": {
        "anti_pattern": "violation de l'ouvert/fermé (O)",
        "remede_minimal": "un registre d'exporteurs, extensible sans modification",
    },
}

POURQUOI_PAS_PLUS = """\
Chaque remède est le PLUS SIMPLE qui lève le symptôme — une injection, une
séparation, un dict. On n'ajoute ni conteneur DI, ni Abstract Factory, ni
couche d'événements : rien ne le justifie aujourd'hui. Penser avant de coder,
choisir en ingénieur, comprendre le coût.
"""


def _checks() -> None:
    assert remedy("algo_varie") == "une fonction (Strategy)"
    assert remedy("couplage_fort") == "abstraction + injection"
    assert len(EXERCICE_1) == 4

    assert set(REVUE) == {
        "config par Singleton global",
        "DB + métier mélangés",
        "export par if rouvert à chaque ajout",
    }
    for entry in REVUE.values():
        assert "anti_pattern" in entry and "remede_minimal" in entry


if __name__ == "__main__":
    _checks()
    print("chapitre 44 — corrigés OK")
