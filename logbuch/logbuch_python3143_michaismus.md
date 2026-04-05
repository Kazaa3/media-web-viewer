# logbuch_python3143_michaismus.md

## Python 3.14.3 Update & Michaismus Helper Tool

**Datum:** 29. März 2026

---

### Zielsetzung

- Umstellung der Media Web Viewer-Laufzeitumgebung auf Python 3.14.3
- Entwicklung eines neuen "Michaismus"-Helper-Skripts für saubere Updates und reproduzierbare Umgebungen

---

### 🛠️ Geplante Änderungen

#### 1. Core Environment Sync (`src/core/main.py`)
- **Version Guard:**
  - Früher Check (Zeile 4): Update auf `(3, 14, 3)`
  - `ensure_stable_environment` (Zeile 78): Update auf `(3, 14, 3)`
  - Fallback-Logik prüft die neue Version

#### 2. Michaismus Helper Tool (`scripts/michaismus_helper.py`)
- **Features:**
  - `clean`: Entfernt rekursiv `__pycache__`, `.pytest_cache`, `build/`, `dist/`, alte `.log`-Dateien
  - `update`: Führt `pip install --upgrade pip` und `pip install -r infra/requirements-core.txt` aus
  - `bootstrap`: Erstellt `.venv_run` und `.venv_core` mit dem Ziel-Python-Binary
  - `diagnostic`: Zeigt Health-Check zu Umgebung und Abhängigkeiten

#### 3. Environment Migration
- Entferne alte `.venv_run` und `.venv_core`
- Erstelle neue venvs mit `/usr/local/bin/python3.14` (da 3.14.3 nicht verfügbar)
- Initialisiere Umgebung mit `pip install -r infra/requirements-core.txt`

---

### ⚠️ Hinweise
- **Python-Binary:** Nur 3.14.0 auf `/usr/local/bin/python3.14` gefunden. Interner Check wird trotzdem auf 3.14.3 gesetzt.
- **Venv-Neuerstellung:** Manuell installierte Pakete gehen verloren, alles wird über `infra/requirements-core.txt` wiederhergestellt.
- **Offene Fragen:**
  - Gibt es weitere generierte Caches (z.B. in `web/streams/` oder `app_data/`), die der Helper bereinigen soll?
  - Ist der Name "Michaismus" ein spezieller Projektbezug?

---

### ✅ Verifikation
- **Automatisiert:**
  - Syntax-Check für alle neuen/angepassten Python- und JS-Dateien
  - Start von `src/core/main.py` prüft neuen Version Guard
- **Manuell:**
  - `clean`-Kommando entfernt Caches
  - `update` installiert alle Abhängigkeiten

---

**Fazit:**
Die geplanten Änderungen sorgen für eine robuste, saubere und zukunftssichere Python-Umgebung. Der "Michaismus"-Helper vereinfacht Wartung und Updates erheblich.

*Letzte Änderung: 29.03.2026*
