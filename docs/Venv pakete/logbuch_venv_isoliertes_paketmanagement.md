# Logbuch: Isoliertes Paketmanagement pro venv (pyenv, pyenv-virtualenv, uv)

## Ziel
Jede Python-Umgebung (venv) verwaltet ihre Zusatzpakete (z.B. pymkv2, enzyme) komplett isoliert und reproduzierbar. Keine globale Pollution, volle Kontrolle über Abhängigkeiten und Versionen.

---

## 1. Pro venv: requirements.txt
- Jede venv hat eigene requirements.txt:
  ```bash
  # venv-3.12 aktiv
  pip install pymkv2 enzyme
  pip freeze > requirements-3.12.txt
  # Später: pip install -r requirements-3.12.txt
  ```
- Vorteil: Jede Umgebung bleibt sauber und reproduzierbar.

---

## 2. pyenv + pyenv-virtualenv (empfohlen für viele Versionen)
- Plugin installieren:
  ```bash
  git clone https://github.com/pyenv/pyenv-virtualenv ~/.pyenv/plugins/pyenv-virtualenv
  ```
- Venv mit Python-Version erstellen:
  ```bash
  pyenv virtualenv 3.12.2 mkv-lib-3.12
  pyenv activate mkv-lib-3.12
  pip install pymediainfo
  pip freeze > requirements.txt
  deactivate
  ```
- Wechseln: `pyenv activate andere-env`
- Vorteil: Automatische Aktivierung, Versionen und Umgebungen klar getrennt.

---

## 3. App-Struktur (Beispiel)
```
media-lib/
├── .python-version
├── envs/
│   ├── mkv-scan/    # pyenv virtualenv 3.12.2 mkv-scan
│   │   └── requirements.txt
│   └── streaming/   # pyenv virtualenv 3.11.9 streaming
│       └── requirements.txt
├── pyproject.toml   # optional (poetry/uv)
└── scripts/
    ├── run_mkv.py
```

---

## 4. Modern: UV (2026-Standard)
- Installation:
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  uv venv mkv-env --python 3.12.2
  source .venv/bin/activate
  uv add pymkv2 enzyme
  uv sync
  ```
- Vorteil: Lockfiles, superschnell, ideal für Teams/Docker.

---

## 5. Best Practices
- Niemals `sudo pip` – immer venv!
- requirements.txt/uv.lock committen, nicht venv/ selbst.
- VS Code: `.vscode/settings.json` → "python.defaultInterpreterPath": "./envs/mkv-scan/bin/python"
- Docker: `COPY requirements.txt . && pip install -r requirements.txt`

---

## Fazit
Mit pyenv, pyenv-virtualenv oder UV verwaltest du Zusatzpakete pro Umgebung/Version – sauber, reproduzierbar, ohne globale Konflikte. UV ist der neue Standard für Lockfiles und schnelle Setups. Siehe auch:
- [realpython: pyenv](https://realpython.com/intro-to-pyenv/)
- [freecodecamp: venv/pyenv](https://www.freecodecamp.org/news/manage-multiple-python-versions-and-virtual-environments-venv-pyenv-pyvenv-a29fb00c296f/)
- [blog.inedo: Best Practices](https://blog.inedo.com/python/python-environment-management-best-practices)
