# Verbesserungen: Environment-Handling & Test-Stabilität

**Datum:** 15.03.2026

## 1. Requirements aus Subfoldern
- **Zentrale Erfassung:** Das Backend (`src/core/main.py`) scannt jetzt sowohl das Projekt-Root als auch das `infra/`-Verzeichnis nach Requirement-Dateien.
- **Rekursive Auflösung:** Ein rekursiver Parser folgt `-r requirements-core.txt`-Redirects, sodass alle Abhängigkeiten auch bei Aufteilung auf mehrere Dateien korrekt erkannt werden.
- **Kompatibilitäts-Link:** Im Projekt-Root gibt es jetzt eine `requirements.txt`, die auf `infra/requirements.txt` verweist. Das verbessert die Kompatibilität mit Standard-Tools (CI/CD, IDEs).

## 2. Stabilisierung Git Actions (CI)
- **Build-System-Resilienz:** `infra/build_system.py` sucht jetzt gezielt nach `pytest` und prüft bei Bedarf spezialisierte venvs (z. B. `.venv_testbed`), falls im aktuellen Interpreter Testpakete fehlen.
- **Redirect-Support:** Die neue Root-`requirements.txt` sorgt dafür, dass GitHub Actions alle Abhängigkeiten automatisch findet und installiert – ohne manuelle Pfadangaben.

## 3. Fixes für das GUI-Test-Tab
- **Umgebungs-Erkennung:** Die Funktion `run_tests` in `src/core/main.py` verlässt sich nicht mehr starr auf die App-Umgebung. Läuft die App in einer "leichten" Umgebung (z. B. `.venv_run`), wird automatisch `.venv_testbed` oder `.venv_dev` gesucht und für Tests verwendet.
- **PYTHONPATH-Integrität:** Beim Testlauf wird der `PYTHONPATH` korrekt gesetzt, sodass Modelle und Parser unabhängig von der gewählten Umgebung importiert werden können.

---

**Ergebnis:**
- Die "Options"-Statusanzeige ist jetzt korrekt.
- Die Test-Suite läuft stabil und zuverlässig – lokal wie in CI/CD.
