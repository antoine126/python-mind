# Penser en Python — corrigés des exercices

Code et **corrigés commentés** des exercices du livre
**« Penser en Python — Des fondations aux architectures avancées »**
(Antoine Pagneux).

Le code vit dans le paquet `src/think_python/`, organisé par chapitre selon
les renvois `chapter-NN/<slug>` du livre. Pour un chapitre donné, le fichier
`solutions.py` contient les corrigés sous forme de **code exécutable, typé et
auto-vérifiant**.

## Démarrage rapide

```bash
# Installer uv si besoin : https://docs.astral.sh/uv/
uv sync                     # crée l'environnement + outils de dev (pytest, ruff)

# Lancer un corrigé isolément (il s'auto-vérifie) :
uv run python src/think_python/chapter-01/modele-mental/solutions.py

# Lancer toute la suite de tests :
uv run pytest

# Lister les chapitres disponibles :
uv run think-python
```

## Comment c'est organisé

```
src/think_python/
  __init__.py                              # petit CLI (`uv run think-python`)
  chapter-01/modele-mental/solutions.py
  chapter-02/pied-a-letrier/solutions.py
  ...
  chapter-44/synthese/solutions.py
tests/test_solutions.py                    # exécute le corrigé de chaque chapitre
```

Chaque `solutions.py` :

- contient les corrigés (un par exercice), avec des commentaires expliquant
  **le raisonnement**, pas seulement la solution ;
- expose une fonction `_checks()` qui **vérifie** les corrigés déterministes
  par des `assert` ;
- est lançable directement — il s'auto-teste et affiche
  `chapitre N — corrigés OK`.

Le fichier `tests/test_solutions.py` découvre tous les
`src/think_python/chapter-*/*/solutions.py` et **exécute chacun comme un
script complet** (bloc `__main__` inclus, qui appelle `_checks()`) : un
chapitre est validé s'il se termine sans erreur. Un seul `uv run pytest`
valide ainsi l'ensemble du dépôt.

## Dépendances optionnelles

La grande majorité des chapitres n'utilise que la **bibliothèque standard**.
Quelques-uns reposent sur des bibliothèques tierces, regroupées en *extras* :

| Extra  | Bibliothèques                                        | Chapitres   |
|--------|------------------------------------------------------|-------------|
| `data` | NumPy, Pandas, Polars                                | 34, 35, 36  |
| `web`  | FastAPI, Pydantic, pydantic-settings, httpx, uvicorn | 24, 32, 33  |

```bash
uv sync --extra data --extra web     # tout installer
uv sync --extra data                 # seulement NumPy/Pandas/Polars
```

Sans ces extras, `uv run pytest` **ignore proprement** les chapitres concernés
(test *skipped*, jamais en échec).

### Lancer les exemples web

Les chapitres 32 et 33 définissent une application FastAPI :

```bash
uv sync --extra web
cd src/think_python/chapter-32/fastapi-routes
uv run uvicorn solutions:app --reload   # http://127.0.0.1:8000/docs
```

## Correspondance avec le livre

Les 44 chapitres suivent les 8 parties de l'ouvrage :

| Partie | Chapitres | Thème                                     |
|--------|-----------|-------------------------------------------|
| I      | 01–08     | Fondations : penser et écrire du Python   |
| II     | 09–13     | Bien écrire : lisibilité, style, qualité  |
| III    | 14–20     | La pensée objet                           |
| IV     | 21–24     | Modéliser les données                     |
| V      | 25–30     | Python idiomatique et performant          |
| VI     | 31–33     | Construire des APIs avec FastAPI          |
| VII    | 34–37     | Manipuler les données (NumPy → Spark)     |
| VIII   | 38–44     | Architecture et design patterns           |

## Conventions

- Python **3.12+** (formes modernes : `list[int]`, `X | None`, `type X = …`,
  `match`, `StrEnum`).
- Code et commentaires en **anglais** dans les exemples « réalistes », prose
  d'explication en **français** (cohérent avec le livre).
- Outillage : `uv` (projet/env), `ruff` (format + lint), `pytest` (tests).
- Le **fil rouge Taskline** (un mini-service de gestion de tâches) traverse les
  corrigés, comme dans le livre.

## Licence

Corrigés pédagogiques accompagnant le livre. Réutilisation libre à des fins
d'apprentissage.
