# Logbuch: Requirements Engineering & Anforderungsmanagement

## Ziel
Systematische Erfassung, Dokumentation und Pflege aller Anforderungen (funktional, nicht-funktional, technischer Kontext). Nachvollziehbarkeit und Priorisierung für Entwicklung, Test und Betrieb.

---

## Vorgehen
1. **Anforderungsquellen:**
   - Stakeholder, Nutzer, Entwickler, Betrieb, Gesetzgebung
2. **Kategorisierung:**
   - Funktionale Anforderungen (Features, Use Cases)
   - Nicht-funktionale Anforderungen (Performance, Sicherheit, Skalierbarkeit, Usability)
   - Technische Anforderungen (Plattform, Schnittstellen, Tools)
3. **Dokumentation:**
   - Logbuch-Einträge, Tickets, User Stories, Spezifikationen
   - Versionierung und Änderungsmanagement
4. **Priorisierung:**
   - Muss-, Soll-, Kann-Anforderungen
   - Business Value, Risiko, Aufwand
5. **Validierung & Verifikation:**
   - Tests, Reviews, Abnahme
   - Traceability (Anforderung → Testfall → Implementierung)
6. **Pflege & Monitoring:**
   - Regelmäßige Überprüfung, Anpassung, Status-Tracking

---

## Scope & Vision

### Vision
- Media Web Viewer als modularer, skalierbarer und performanter Medienmanager für Desktop und Web
- Klare Trennung von Kernlogik, Parser-Pipeline, CLI, UI und Testumgebungen
- Maximale Erweiterbarkeit, Isolation und Nachvollziehbarkeit
- Zukunftssichere Architektur: Multi-Core, Multi-User, CI/CD, Docker, moderne Python-Versionen
- Fokus auf Usability, Performance, Transparenz und Automatisierung

### Scope
- Funktionale Anforderungen: Medienanalyse, Bibliotheksmanagement, Playback, Metadaten-Extraktion, Logging, API
- Nicht-funktionale Anforderungen: Performance, Skalierbarkeit, Sicherheit, Zuverlässigkeit, Usability
- Technischer Scope: Python 3.14+, Multi-Venv, Docker, CI/CD, moderne Parser-Tools, Data Science Integration
- Dokumentation: Logbuch, Architektur, Testpläne, Requirements Engineering
- Test-Suite: Health, Performance, Smoke, E2E, Backend-Frontend-Sync, Parallelität, Regression

---

## Best Practices
- Anforderungen klar, messbar und testbar formulieren
- Änderungen transparent und nachvollziehbar dokumentieren
- Stakeholder regelmäßig einbinden
- Automatisierte Tools für Traceability und Status-Tracking nutzen

---

## Akzeptanztests, Testfälle & Unit Tests

### Akzeptanztests
- Validieren, ob die implementierten Features und Anforderungen den Erwartungen der Stakeholder entsprechen
- Szenarien: End-to-End-Tests, User Stories, Use Cases, GUI-Interaktion, Medienanalyse
- Dokumentation: Akzeptanzkriterien, Testprotokolle, Abnahme durch Stakeholder

### Testfälle
- Systematische Testfall-Erstellung für alle Anforderungen (funktional/nicht-funktional)
- Testfall-Typen: Health, Performance, Smoke, E2E, Regression, Parallelität, Fehlerhandling
- Traceability: Anforderung → Testfall → Implementierung
- Dokumentation: Logbuch, Testplan, automatisierte Tests

### Unit Tests
- Isolierte Tests für einzelne Funktionen, Klassen und Module
- Ziel: Korrektheit, Robustheit, Fehlerfreiheit auf Code-Ebene
- Tools: pytest, unittest, Coverage
- Integration in CI/CD Pipeline
- Dokumentation: Testabdeckung, Fehlerberichte, Regressionstests

---

## Fehlerberichte & Regressionstests

### Fehlerberichte
- Systematische Erfassung und Dokumentation von Fehlern (Bug Reports, Issues)
- Inhalte: Fehlerbeschreibung, Reproduktionsschritte, Logs, Screenshots, betroffene Komponenten
- Nachverfolgung: Status, Priorität, Verantwortlicher, Lösung
- Integration: Logbuch, Issue Tracker, CI/CD Alerts

### Regressionstests
- Automatisierte Tests zur Sicherstellung, dass neue Änderungen keine bestehenden Funktionen beeinträchtigen
- Testfall-Auswahl: Alle kritischen und betroffenen Bereiche
- Integration in CI/CD Pipeline: Jeder Build/Release wird automatisch getestet
- Dokumentation: Regressionstestplan, Fehlerhistorie, Testabdeckung
- Ziel: Stabilität, Zuverlässigkeit, kontinuierliche Qualitätssicherung

---

## Akzeptanzkriterien & Testprotokolle

### Akzeptanzkriterien
- Klare, messbare Kriterien für die Abnahme von Features und Anforderungen
- Erfüllt, wenn:
  - Funktionalität wie spezifiziert vorhanden ist
  - Performance und Zuverlässigkeit den Vorgaben entsprechen
  - Fehlerhandling und Usability nachgewiesen sind
  - Dokumentation und Nachvollziehbarkeit gegeben sind
- Beispiele:
  - "Medienanalyse funktioniert für alle unterstützten Dateitypen ohne Fehler."
  - "Parser-Pipeline kann parallel laufen und liefert korrekte Ergebnisse."
  - "Logs und Fehlerberichte sind vollständig und nachvollziehbar."

### Testprotokolle
- Strukturierte Dokumentation der Testergebnisse
- Inhalte:
  - Testfall, Datum, Tester, Umgebung
  - Ergebnis (Bestanden/Nicht bestanden), Fehler, Screenshots, Logs
  - Abweichungen, Kommentare, Nachtests
- Ablage: Logbuch, Testplan, automatisierte Reports (CI/CD)
- Nachvollziehbarkeit: Jeder Akzeptanztest ist dokumentiert und kann nachvollzogen werden

---

## Komponenten-Gesamttest & Teststufen

### Komponenten-Gesamttest
- Integrationstest aller Hauptkomponenten: Core, Parser-Pipeline, CLI, UI, Datenbank, Logging, API
- Ziel: Zusammenspiel, Schnittstellen, Fehlerhandling und Performance im Gesamtsystem
- Szenarien: End-to-End-Tests, Multi-User, Parallelbetrieb, Medienanalyse, Synchronisation
- Dokumentation: Testprotokolle, Abnahme, Fehlerberichte

### Teststufen
1. **Unit Test:**
   - Einzelne Funktionen, Klassen, Module
   - Tools: pytest, unittest
2. **Integrationstest:**
   - Zusammenspiel mehrerer Komponenten/Module
   - Schnittstellen, Datenfluss, Fehlerhandling
3. **Systemtest:**
   - Gesamtsystem (alle Komponenten)
   - End-to-End, Performance, Usability, Sicherheit
4. **Abnahmetest (Akzeptanztest):**
   - Validierung durch Stakeholder
   - User Stories, Use Cases, GUI, Medienanalyse
5. **Regressionstest:**
   - Sicherstellung, dass Änderungen keine bestehenden Funktionen beeinträchtigen
   - Automatisiert in CI/CD

---

## Ressourcen & Zeitmanagement

### Kontext
- Das Projekt ist ein Hobbyprojekt, um neue Technologien, Architektur- und Testmethoden kennenzulernen und praktisch zu erproben.
- Fokus liegt auf Lernen, Experimentieren und kontinuierlicher Verbesserung.

### Ressourcen
- Zeit: Flexible Einteilung, keine festen Deadlines
- Team: Einzelperson oder kleine Gruppe, freiwillige Beiträge
- Tools: Moderne Python-Versionen, Data Science Libraries, CI/CD, Docker, neue Parser-Technologien

### Zeitmanagement
- Iteratives Vorgehen: Kleine, abgeschlossene Arbeitspakete
- Priorisierung nach Lerninteresse und Machbarkeit
- Dokumentation und Reflektion im Logbuch
- Keine Überlastung, Pausen und Motivation im Vordergrund

### Lernziele
- Praktische Erfahrung mit Requirements Engineering, Testautomatisierung, Multi-Core-Architektur, CI/CD
- Experimentieren mit neuen Features, Frameworks und Tools
- Dokumentation und Austausch von Erkenntnissen

---

## Testergebnisse & Reports

### Testergebnisse
- Ergebnisse aller Tests (Unit, Integration, System, Akzeptanz, Regression) werden strukturiert erfasst
- Inhalte: Testfall, Status (Bestanden/Nicht bestanden), Fehler, Logs, Screenshots, Datum, Tester
- Automatisierte Tests: Ergebnisse als Report (HTML, XML, JSON) aus CI/CD
- Manuelle Tests: Protokolle im Logbuch oder als Markdown

### Reports
- Automatisierte Generierung von Testberichten nach jedem Testlauf
- Formate: HTML, PDF, Markdown, JSON, CI/CD-Dashboard
- Inhalte: Zusammenfassung, Detailansicht, Fehlerstatistik, Testabdeckung, Trends
- Ablage: Logbuch, CI/CD-Reports, Projekt-Dokumentation
- Nachvollziehbarkeit: Jeder Test und Report ist versioniert und dokumentiert

---

## Dashboards & Data Science

### Dashboards
- Visualisierung der Testergebnisse, Fehlerstatistik und Projektstatus in interaktiven Dashboards
- Tools: CI/CD-Dashboard, Grafana, Plotly Dash, Streamlit, Jupyter Notebooks
- Inhalte: Testabdeckung, Trends, Performance, Fehlerhäufigkeit, Status aller Komponenten
- Integration: Automatisierte Reports, Live-Daten aus Testläufen und Logsystem

### Data Science
- Analyse und Visualisierung von Testdaten, Performance-Messungen und Fehlerberichten
- Tools: Pandas, Numpy, Matplotlib, Seaborn, Plotly
- Ziele: Muster erkennen, Optimierungspotenziale identifizieren, statistische Auswertungen
- Beispiele: Heatmaps, Boxplots, Zeitreihen, Korrelationen zwischen Fehlern und Performance
- Dokumentation: Ergebnisse und Erkenntnisse im Logbuch, als Grafiken und Data Science Notebooks

---

## Web-GUI & Gekapselter Betrieb

### Web-GUI
- Separate, moderne Web-GUI für Medienverwaltung, Analyse und Visualisierung
- Technologien: HTML, JS, Eel, Flask/Bottle, moderne Frameworks (z.B. React, Vue)
- Features: Medienbibliothek, Playback, Metadatenanzeige, Dashboard, Fehlerberichte, Teststatus
- Integration: API-Anbindung, Echtzeit-Updates, Benutzerverwaltung
- Dokumentation: Architektur, Schnittstellen, Testfälle, Usability-Kriterien

### Gekapselter Betrieb an zwei Orten
- Betrieb des Media Web Viewer an mehreren, voneinander unabhängigen Standorten (z.B. Home und Office)
- Gekapselte Umgebungen: Separate venvs, Datenbanken, Logsysteme, Konfigurationen
- Synchronisation: Export/Import von Medienbibliothek, Einstellungen, Logs
- Ziel: Maximale Isolation, Datenschutz, flexible Nutzung
- Dokumentation: Setup, Betrieb, Synchronisations-Workflow, Testfälle für Multi-Standort-Betrieb

---

**Stand:** 12. März 2026
