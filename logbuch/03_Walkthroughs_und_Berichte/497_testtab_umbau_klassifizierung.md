# Logbuch: Umbau Test-Tab & Testklassifizierung (2026-03-15)

## 1. Ziel des Umbaus
- Der Test-Tab wird neu gestaltet, um die aktuelle Teststrategie und Testklassifizierung besser abzubilden.
- Fokus: Übersichtlichkeit, gezielte Testauswahl, klare Trennung der Testarten.

## 2. Neue Struktur des Test-Tabs
- **Testarten als Reiter oder Filter:**
  - Unit-Tests (Modul-/Komponententests)
  - Integrationstests (Zusammenspiel mehrerer Module)
  - End-to-End-Tests (E2E, UI/Workflow)
  - Spezialtests (z.B. Performance, Regression, UI-Visual)
- **Teststatus-Anzeige:**
  - Übersichtliche Darstellung: bestanden, fehlgeschlagen, übersprungen
  - Farbliche Markierung (z.B. grün/rot/grau)
- **Testauswahl & -ausführung:**
  - Filter nach Testart, Komponente, zuletzt geändert
  - Einzelne Tests oder Testgruppen gezielt starten
- **Testdetails:**
  - Ausführliche Fehlerausgabe, Stacktrace, ggf. Screenshot bei UI-Tests
  - Verlinkung zu zugehörigen Logbuch-Einträgen oder Code-Stellen

## 3. UI-Skizze (Beispiel)
```
+-------------------------------------------------------------+
| Tests: [Unit] [Integration] [E2E] [Spezial] [Alle]           |
+-------------------------------------------------------------+
| [Suchfeld]   [Filter: Komponente/Status]   [Tests starten]   |
+-------------------------------------------------------------+
| Testname        | Typ     | Status   | Details/Logs          |
|-----------------|---------|----------|-----------------------|
| test_logging    | Unit    | ✔️       | [Details]             |
| test_debug_flag | Unit    | ❌       | [Details]             |
| ...             | ...     | ...      | ...                   |
+-------------------------------------------------------------+
```

## 4. Technische Hinweise
- Testtab-Logik und UI werden im Frontend (web/app.html, JS) angepasst.
- Backend liefert Teststatus, Fehlerdetails und Testklassifizierung (API: `/get_test_status` etc.).
- Testklassifizierung erfolgt über Metadaten/Tags in den Testdateien.

## 5. Vorteile der neuen Struktur
- Schnellere Fehleranalyse durch gezielte Filterung
- Klare Übersicht über Testabdeckung und -status
- Bessere Nachvollziehbarkeit der Teststrategie im UI

## 6. ToDo
- Testtab-UI umbauen (Reiter, Filter, Statusanzeige)
- Backend-API für Teststatus/Testarten erweitern
- Testklassifizierung in Testdateien und API abbilden
- Dokumentation und Logbuch-Einträge verlinken

## 7. Feature: Modal – Rückkehr zur Dokumentenübersicht
- Das Modal-Feature im Test-Tab zeigte ursprünglich die wichtigsten Dokumente im relevanten Ordner (z.B. README, CHANGELOG, TEST_SUITES.md, ARCHITEKTUR.md).
- Nach dem Refactoring und einem Fehler wurde temporär eine Basic-Version implementiert, die nur die letzten 3 Dokumente/Logik anzeigte.
- **Anpassung:**
  - Das Modal-Feature wird wieder so angepasst, dass es gezielt die wichtigsten Dokumente im Ordner anzeigt (wie ursprünglich).
  - Die Anzeige der letzten 3 Dokumente wird entfernt bzw. durch die gezielte Auswahl der wichtigsten Dateien ersetzt.
- **Vorteile:**
  - Schnellzugriff auf zentrale Projektdokumente direkt aus dem Test-Tab
  - Bessere Orientierung und Dokumentationsintegration für Entwickler und Tester
- **ToDo:**
  - Modal-Logik im Test-Tab anpassen: gezielte Auswahl und Anzeige der wichtigsten Dokumente
  - Basic-Logik (letzte 3 Dateien) entfernen
  - UI/UX-Tests für die neue/alte Dokumentenübersicht im Modal

## 8. Projektmanagement & Professionalisierung
- Im Zuge des Testtab-Umbaus und der UI-Modernisierung wird das Projektmanagement weiter professionalisiert.
- **Maßnahmen:**
  - Einführung klarer Rollen (z.B. Maintainer, Reviewer, QA, DevOps)
  - Nutzung von Issue- und Feature-Templates für strukturierte Aufgabenverfolgung
  - Regelmäßige Review- und Testzyklen (z.B. Pull-Request-Reviews, automatisierte Test-Gates)
  - Dokumentationspflicht für alle relevanten Änderungen (Logbuch, Changelog, Architektur)
  - CI/CD-Pipeline mit Build-, Test- und Release-Gates
  - Definition von Coding-Standards und Styleguides
  - Einführung von Release- und Milestone-Planung
- **Vorteile:**
  - Höhere Codequalität und Nachvollziehbarkeit
  - Schnellere Fehlererkennung und -behebung
  - Bessere Zusammenarbeit im Team
  - Klare Verantwortlichkeiten und strukturierte Abläufe
- **ToDo:**
  - Projektmanagement-Tools und Templates einführen/aktualisieren
  - Review- und Testprozesse dokumentieren und etablieren
  - Regelmäßige Retrospektiven und Verbesserungszyklen