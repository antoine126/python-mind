"""Vérifie que le code de CHAQUE chapitre se lance bien.

Chaque ``src/think_python/chapter-NN/<slug>/solutions.py`` est exécuté comme un
script à part entière (avec son bloc ``if __name__ == "__main__"``, qui appelle
ses auto-vérifications ``_checks()``). Un chapitre est validé s'il se termine
avec un code de retour 0.

Les chapitres qui dépendent de bibliothèques tierces (NumPy, Pandas, Polars,
Pydantic, FastAPI) sont ignorés proprement si la dépendance n'est pas installée
— voir ``uv sync --extra data`` / ``--extra web``.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

CHAPTERS_DIR = Path(__file__).resolve().parent.parent / "src" / "think_python"
SOLUTION_FILES = sorted(CHAPTERS_DIR.glob("chapter-*/*/solutions.py"))


@pytest.mark.parametrize("path", SOLUTION_FILES, ids=lambda p: p.parent.name)
def test_chapter_solution_runs(path: Path) -> None:
    """Exécute le corrigé du chapitre et vérifie qu'il se lance sans erreur."""
    result = subprocess.run(
        [sys.executable, str(path)],
        capture_output=True,
        text=True,
        cwd=path.parent,
    )
    if result.returncode != 0:
        if "ModuleNotFoundError" in result.stderr:
            missing = result.stderr.rsplit("'", 2)[-2] if "'" in result.stderr else "?"
            pytest.skip(f"dépendance optionnelle manquante : {missing}")
        pytest.fail(
            f"{path.parent.name} a échoué (code {result.returncode}) :\n"
            f"{result.stderr}"
        )
    assert "OK" in result.stdout, f"sortie inattendue : {result.stdout!r}"


def test_all_chapters_present() -> None:
    """Les 44 chapitres du livre doivent avoir un corrigé."""
    assert len(SOLUTION_FILES) == 44, f"trouvé {len(SOLUTION_FILES)} corrigés / 44"
