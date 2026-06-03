"""Corrigés et exemples de code du livre « Penser en Python »."""

from __future__ import annotations

from pathlib import Path

__all__ = ["main"]


def main() -> None:
    """Liste les chapitres dont les corrigés sont disponibles dans le dépôt."""
    pkg = Path(__file__).resolve().parent          # src/think_python
    repo = pkg.parents[1]                          # racine du dépôt
    chapters = sorted(p.parent for p in pkg.glob("chapter-*/*/solutions.py"))
    print("Penser en Python — corrigés des exercices\n")
    if not chapters:
        print("Aucun corrigé trouvé.")
        return
    for chapter in chapters:
        rel = chapter.relative_to(repo)
        print(f"  uv run python {rel}/solutions.py")
    print(f"\n{len(chapters)} chapitres. Lancez les tests avec : uv run pytest")
