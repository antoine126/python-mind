"""Chapitre 23 — Enum, IntEnum, StrEnum, Flag : corrigés."""

from __future__ import annotations

from enum import Enum, Flag, auto


# ---------------------------------------------------------------------------
# Exercice 1 — Refaire : éliminer les chaînes magiques
# ---------------------------------------------------------------------------
class Role(Enum):
    ADMIN = "admin"
    USER = "user"


def can_delete(role: Role) -> bool:
    """`is` : les membres sont des singletons ; pas de chaîne à mal écrire."""
    return role is Role.ADMIN


# ---------------------------------------------------------------------------
# Exercice 2 — Comprendre : Enum ou IntEnum
# ---------------------------------------------------------------------------
EXERCICE_2 = {
    "a) statuts d'une tâche, jamais sérialisés tels quels": "Enum pur — pas "
    "d'interop int/str ; le double statut serait un risque pour rien.",
    "b) codes de réponse HTTP": "IntEnum — les codes SONT des entiers (200…) "
    "et interopèrent avec des bibliothèques HTTP.",
    "c) niveau de log sérialisé en chaîne JSON": "StrEnum — se sérialise "
    "directement en \"INFO\" sans conversion.",
}


# ---------------------------------------------------------------------------
# Exercice 3 — Concevoir : permissions de Taskline (Flag, cumulables)
# ---------------------------------------------------------------------------
class Permission(Flag):
    READ = auto()
    WRITE = auto()
    SHARE = auto()
    ADMIN = auto()


EDITOR = Permission.READ | Permission.WRITE
SUPERUSER = Permission.READ | Permission.WRITE | Permission.SHARE | Permission.ADMIN


def can(role: Permission, perm: Permission) -> bool:
    return perm in role            # test d'appartenance sur un Flag


def _checks() -> None:
    assert can_delete(Role.ADMIN) is True
    assert can_delete(Role.USER) is False
    assert [r.value for r in Role] == ["admin", "user"]   # itérable

    assert can(EDITOR, Permission.WRITE) is True
    assert can(EDITOR, Permission.ADMIN) is False
    assert can(SUPERUSER, Permission.ADMIN) is True


if __name__ == "__main__":
    _checks()
    print("chapitre 23 — corrigés OK")
