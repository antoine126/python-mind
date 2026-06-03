"""Chapitre 31 — Le modèle mental d'une API web : corrigés.

Exercices de conception REST (ressources, méthodes, statuts) : stdlib, sans
framework. FastAPI est utilisé aux chapitres 32 et 33.
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Exercice 1 — Refaire : des routes RESTful
# ---------------------------------------------------------------------------
# Ressource dans l'URL, action dans la méthode, GET toujours « sûr ».
EXERCICE_1 = {
    "GET /createTask": ("POST", "/tasks", 201),
    "GET /deleteTask?id=5": ("DELETE", "/tasks/5", 204),
    "POST /getAllTasks": ("GET", "/tasks", 200),
}


# ---------------------------------------------------------------------------
# Exercice 2 — Comprendre : le bon statut
# ---------------------------------------------------------------------------
def status_for(scenario: str) -> int:
    """La famille (2xx/4xx/5xx) dit d'abord succès / faute client / faute serveur."""
    return {
        "task_created": 201,            # ressource créée
        "task_missing": 404,            # demande d'une ressource inexistante
        "malformed_body": 400,          # (ou 422 en FastAPI) entrée invalide
        "unhandled_exception": 500,     # plantage côté serveur
        "deleted_no_content": 204,      # succès, rien à renvoyer
    }[scenario]


# ---------------------------------------------------------------------------
# Exercice 3 — Concevoir : l'API de Taskline
# ---------------------------------------------------------------------------
TASKLINE_API = [
    ("GET", "/tasks", 200),            # lister
    ("POST", "/tasks", 201),           # créer (corps JSON validé par Pydantic)
    ("GET", "/tasks/{id}", 200),       # lire une (ou 404)
    ("PATCH", "/tasks/{id}", 200),     # marquer terminée (ou 404)
    ("DELETE", "/tasks/{id}", 204),    # supprimer
]


def _checks() -> None:
    assert EXERCICE_1["GET /createTask"] == ("POST", "/tasks", 201)
    assert EXERCICE_1["GET /deleteTask?id=5"][0] == "DELETE"

    assert status_for("task_created") == 201
    assert status_for("task_missing") == 404
    assert status_for("unhandled_exception") == 500
    assert status_for("deleted_no_content") == 204

    methods = {route[0] for route in TASKLINE_API}
    assert methods == {"GET", "POST", "PATCH", "DELETE"}


if __name__ == "__main__":
    _checks()
    print("chapitre 31 — corrigés OK")
