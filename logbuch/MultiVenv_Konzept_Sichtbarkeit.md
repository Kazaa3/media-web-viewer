# Multi-Venv-Konzept und Sichtbarkeit

## Hintergrund
Nach Abschluss von Milestone 7 (Build-System und Code Quality Cleanup) wurde festgestellt, dass die Sichtbarkeit und Dokumentation der verschiedenen Python-venv-Umgebungen im UI und in der Projektstruktur nicht ausreichend ist. Die bisherige venv-Erkennung meldet nur existierende Umgebungen und blendet geplante oder fehlende venvs aus.

---

## Verbesserungen
- Die Funktion get_venv_summary in main.py wurde erweitert, um eine vollständige Übersicht aller venvs (core, testbed, build) zu liefern.
- Die Multi-Venv-Strategie wird im UI und in der Dokumentation klar kommuniziert.
- Status aller venvs (vorhanden/nicht vorhanden/geplant) wird angezeigt.
- Logger-Ausgaben wurden vereinheitlicht, um Diagnosen und Statusmeldungen nachvollziehbar zu machen.

---

## Beispiel-Ausgabe (UI/CLI)

```
Multi-Venv Strategy:
- core: vorhanden (aktiv)
- testbed: nicht vorhanden (geplant)
- build: vorhanden

Hinweis: Die 'core'-Umgebung ist für den Produktivbetrieb, 'testbed' für Integrationstests und 'build' für CI/CD.
```

---

## Weiteres Vorgehen
- Dokumentation der Multi-Venv-Strategie in README.md und DOCUMENTATION.md ergänzen.
- Automatisierte Prüfung und Reporting aller venvs in main.py und manage_venvs.py.
- UI-Komponente für venv-Status und Strategie einführen.

---

## Erweiterung: CLI-Umgebungen und Trennung von 'core' und Entwicklungsumgebung

Um die Trennung zwischen Produktiv- und Entwicklungsumgebung weiter zu stärken, wird empfohlen:
- Die CLI-Umgebung explizit zu erweitern, sodass 'core' (Produktivbetrieb) und 'dev' (Entwicklung/Tests) klar getrennt sind.
- CLI-Befehle und Umgebungsvariablen so gestalten, dass sie die jeweilige venv eindeutig adressieren (z.B. --env core, --env dev).
- Automatisierte Checks und Statusanzeigen für beide Umgebungen im UI und CLI implementieren.
- Dokumentation und Beispiele für die Nutzung beider Umgebungen ergänzen.

Vorteile:
- Klare Verantwortlichkeiten und weniger Risiko von Vermischung.
- Einfachere CI/CD-Integration und Debugging.
- Bessere Nachvollziehbarkeit für Entwickler und Reviewer.

---

## 4. Multi-Venv Concept & Visibility

- UI Reporting: Die Funktion get_venv_summary() zeigt jetzt alle geplanten venvs (.venv_core, .venv_build, etc.) an – auch wenn sie fehlen. Dadurch entsteht eine klare Übersicht der Environment-Strategie.
- Architectural Documentation: In docs/TECH_STACK.md gibt es nun einen eigenen Abschnitt zur Multi-Venv-Strategie, der die Rolle jeder Umgebung erläutert.
- Helper Functions: Kritische Logik wie _extract_key_from_obj wurde wiederhergestellt, um undefined name errors zu beheben.

---

**Letzte Aktualisierung:** 13. März 2026


## Erweiterung: venv dev2

Um die Multi-Venv-Strategie weiter auszubauen, wird die Einführung einer zusätzlichen Entwicklungsumgebung 'venv_dev2' empfohlen:
- Zweck: Separate Entwicklungs-/Testumgebung für experimentelle Features oder parallele Entwicklung.
- Statusanzeige: get_venv_summary() und UI sollten auch 'venv_dev2' berücksichtigen (vorhanden/nicht vorhanden/geplant).
- Dokumentation: Rolle und Nutzung von 'venv_dev2' in TECH_STACK.md und DOCUMENTATION.md ergänzen.
- CLI/Helper: Automatisierte Checks und Umschaltung zwischen venv_dev2 und anderen Umgebungen ermöglichen.

Vorteile:
- Parallele Entwicklung ohne Risiko für Hauptumgebung.
- Bessere Testbarkeit und Flexibilität.