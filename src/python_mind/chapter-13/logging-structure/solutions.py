"""Chapitre 13 — Journalisation, configuration et structure : corrigés."""

from __future__ import annotations

import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Exercice 1 — Refaire : du print au logging
# ---------------------------------------------------------------------------
def run_import(line: str) -> None:
    logger.info("starting import")
    logger.error("could not parse line: %s", line)   # niveau ERROR
    logger.info("import finished, %d errors", 0)


# ---------------------------------------------------------------------------
# Exercice 2 — Comprendre : pourquoi le formatage paresseux
# ---------------------------------------------------------------------------
EXERCICE_2 = """\
`logger.debug("state %s", heavy())` ET `logger.debug(f"state {heavy()}")`
appellent TOUS DEUX heavy() : les arguments sont évalués avant l'appel.
Le formatage paresseux (`%s`) évite seulement l'ASSEMBLAGE de la chaîne
quand le message est filtré. Pour éviter aussi un calcul lourd, il faut une
garde : `if logger.isEnabledFor(logging.DEBUG): logger.debug("state %s", heavy())`.
La f-string est doublement coûteuse (appel + assemblage), d'où la préférence
du formatage différé pour le logging.
"""


# ---------------------------------------------------------------------------
# Exercice 3 — Concevoir : sortir la config du code
# ---------------------------------------------------------------------------
@dataclass
class Settings:
    """Distingue requis / secret / défaut sûr.

    En vrai projet, on utiliserait pydantic-settings pour lire et valider
    l'environnement, et échouer tôt si un requis manque (cf. chapitre 24).
    """

    database_url: str             # requis (pas de défaut)
    api_key: str                  # SECRET, depuis l'environnement
    log_level: str = "INFO"       # défaut sûr, surchargeable
    max_retries: int = 3          # défaut sûr


def _checks() -> None:
    # Capture des enregistrements de log pour vérifier niveaux et messages.
    records: list[logging.LogRecord] = []

    class _Capture(logging.Handler):
        def emit(self, record: logging.LogRecord) -> None:
            records.append(record)

    handler = _Capture()
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    try:
        run_import("bad,line")
    finally:
        logger.removeHandler(handler)

    levels = [r.levelname for r in records]
    assert levels == ["INFO", "ERROR", "INFO"]
    assert records[1].getMessage() == "could not parse line: bad,line"

    s = Settings(database_url="postgres://x", api_key="secret")
    assert s.log_level == "INFO" and s.max_retries == 3


if __name__ == "__main__":
    _checks()
    print("chapitre 13 — corrigés OK")
