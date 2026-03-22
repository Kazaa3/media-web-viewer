# Fixes: Test-Umgebungs-Erkennung & Requirements-Tracking

**Datum:** 15.03.2026

## 1. Fix: Test Environment Discovery
- **Problem:** "No module named pytest" entstand, weil Tests im leichten `.venv_run`-Environment ausgeführt wurden, das keine Testpakete enthält.
- **Lösung:**
  - Die Backend-Logik sucht jetzt explizit nach `.venv_testbed`, `.venv_dev` oder `venv` im Projekt-Root.
  - **Automatisches Umschalten:** Befindet sich die App in `.venv_run`, wird für Testläufe automatisch der Python-Interpreter von `.venv_testbed` (mit pytest/selenium) verwendet.
  - **Sicheres Fallback:** Nur wenn keine spezialisierte venv gefunden wird, wird der aktuelle Interpreter genutzt – so werden "module not found"-Fehler vermieden.

## 2. Fix: Requirements-Tracking in "Options"
- **Rekursives Parsing:** Die Statusprüfung folgt jetzt korrekt allen `-r requirements-core.txt`-Redirects.
- **Multi-Folder-Scan:** Es werden sowohl das Projekt-Root als auch das `infra/`-Verzeichnis nach Requirement-Dateien durchsucht, damit die "fehlende Pakete"-Liste im UI immer stimmt.
- **Root-Kompatibilität:** Eine neue `requirements.txt` im Projekt-Root verweist auf die Datei im `infra/`-Ordner. Das verbessert die Kompatibilität mit GitHub Actions und lokalen IDEs.

---

**Ergebnis:**
- Die Test-Tab-Umgebung ist robust und wählt immer die beste verfügbare venv.
- Die Options-Tab-Anzeige für Requirements ist jetzt vollständig und korrekt.
