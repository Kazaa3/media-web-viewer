# Das 7-Venv-Konzept: Übersicht & Zweck

**Stand: 14.03.2026**

## Ziel
Das 7-Venv-Konzept sorgt für eine saubere Trennung von Entwicklungs-, Test- und Build-Umgebungen im Media Web Viewer. Jede virtuelle Umgebung (venv) erfüllt einen klar definierten Zweck und verhindert Abhängigkeitskonflikte.

---

## Die sieben venvs im Überblick

| Name             | Zweck / Inhalt                                              |
|------------------|------------------------------------------------------------|
| .venv_core       | Minimale Kernabhängigkeiten für den Betrieb (Produktiv)     |
| .venv_build      | Build-Tools, Paketierung, Linting, Type-Checks              |
| .venv_dev        | Entwicklungsumgebung: Debugging, Hot-Reload, Dev-Tools      |
| .venv_testbed    | Testumgebung für Unit- und Integrationstests                |
| .venv_selenium   | Spezielle Umgebung für Selenium/GUI-Tests                   |
| .venv_run        | "Saubere" Laufzeitumgebung für Entwickler (requirements-run.txt) |
| venv             | Legacy-Kompatibilität, zeigt auf root-requirements.txt      |

---

## Details zu den einzelnen venvs

- **.venv_core**: Enthält nur die für den Produktivbetrieb notwendigen Pakete. Wird für minimale, schnelle Deployments genutzt.
- **.venv_build**: Beinhaltet alle Tools für Build, Linting, Type-Checks und Paketierung (z.B. PyInstaller, wheel, mypy, ruff).
- **.venv_dev**: Für die tägliche Entwicklung. Enthält Debug-Tools, Hot-Reload, erweiterte Dev-Abhängigkeiten.
- **.venv_testbed**: Isolierte Umgebung für Unit- und Integrationstests. Verhindert Seiteneffekte durch Entwicklungs- oder Build-Tools.
- **.venv_selenium**: Speziell für End-to-End- und GUI-Tests mit Selenium/Webdriver. Getrennte Browser- und Testabhängigkeiten.
- **.venv_run**: "Saubere" Umgebung für Entwickler, die das Projekt ausführen wollen, ohne Build- oder Testtools. Installiert aus infra/requirements-run.txt.
- **venv**: Für Legacy-Tools und maximale Kompatibilität. Zeigt auf das klassische requirements.txt im Root.

---

## Vorteile
- **Isolation:** Keine Konflikte zwischen Build-, Test- und Laufzeit-Abhängigkeiten
- **Reproduzierbarkeit:** Klare, dokumentierte Abhängigkeitslisten pro Use-Case
- **Schnelle Fehleranalyse:** Fehler lassen sich gezielt auf eine Umgebung eingrenzen
- **Kompatibilität:** Legacy-Tools funktionieren weiterhin über `venv`

---

## Fazit
Das 7-Venv-Konzept ist die Basis für eine stabile, wartbare und skalierbare Entwicklungs- und Build-Infrastruktur im Media Web Viewer.
