# Logbuch: Test Suite PID-Systemtools-GUI

## Übersicht
Die Test Suite für die PID-Anzeige und Prozesskontrolle von Systemtools (ffmpeg, vlc, browser) in der App-GUI deckt zahlreiche Szenarien ab:
- Reale und Mock-Tests für PID-Erfassung, Sichtbarkeit, Debugging, Fehlerbehandlung, Resource Cleanup, Permission Denied, Environment Variables, Stress-Tests.

## Offene Punkte für weitere Tests
- Echte Systemtools (ffmpeg, vlc, Browser) mit realen Kommandos
- Integrationstests mit echter GUI-Kommunikation (API-Endpunkt, UI-Feedback)
- Fehlerfälle wie Zombie-Prozesse, Prozessabsturz, unerwartetes Verhalten
- Performance- und Logging-Tests (Audit-Trail, Multi-User, Cross-Plattform)

## Erweiterungsmöglichkeiten
Die Suite ist praxisnah und kann flexibel erweitert werden, um alle relevanten Szenarien abzudecken.

---

## Integrationstests
- Test: API-Endpunkt für PID-Übermittlung an die GUI
- Test: UI-Feedback bei Prozessstart und -ende (PID-Anzeige, Status-Update)
- Test: Synchronisation zwischen Backend und Frontend (PID, Logs, Status)
- Test: Fehlerhandling im UI bei nicht erreichbaren oder abgestürzten Prozessen
- Test: End-to-End-Test für Prozessstart, PID-Erfassung, Übergabe und Anzeige in der GUI
- Test: Multi-User-Integration (gleichzeitige Prozesse, getrennte Sessions)

**Erfolgskriterien:**
- PIDs werden korrekt vom Backend an die GUI übergeben und angezeigt
- UI reagiert zuverlässig auf Prozessstatus und Fehler
- Synchronisation und Isolation bleiben auch bei parallelen und Multi-User-Szenarien erhalten

**Stand:** 12. März 2026

---

## Parser-Pipeline Tests
- Test: PID-Erfassung und Anzeige für Parser-Prozesse (z.B. ffprobe, mutagen, mediainfo)
- Test: Übergabe der PID von Parser-Prozessen an die GUI (API-Endpunkt, UI-Info)
- Test: Synchronisation und Logging der Parser-PIDs im globalen Logsystem
- Test: Fehlerhandling bei Parser-Absturz oder Timeout
- Test: End-to-End-Test für Parser-Workflow: Datei einlesen → Parser starten → PID erfassen → Ergebnis und PID in der GUI anzeigen
- Test: Multi-Parser-Integration (gleichzeitige Verarbeitung mehrerer Dateien/Prozesse)

**Erfolgskriterien:**
- Parser-PIDs werden korrekt erfasst, geloggt und in der GUI angezeigt
- Fehler und Timeouts werden sauber im UI und Logsystem behandelt
- Synchronisation und Isolation bleiben auch bei parallelen Parser-Prozessen erhalten

---

## Datenbank-Tests
- Test: PID-Erfassung und Speicherung von Systemtools/Parser-Prozessen in der Datenbank
- Test: Korrekte Zuordnung von PID, Prozessname, Startzeit und Status in der DB
- Test: Synchronisation zwischen Logsystem, GUI und Datenbank (PID, Status, Fehler)
- Test: Fehlerhandling bei DB-Operationen (z.B. Schreib-/Lesefehler, Inkonsistenzen)
- Test: End-to-End-Test: Prozessstart → PID erfassen → DB speichern → GUI anzeigen → Status aktualisieren
- Test: Multi-User- und Multi-Prozess-Szenarien (gleichzeitige Einträge, parallele Sessions)

**Erfolgskriterien:**
- PIDs und Prozessdaten werden korrekt in der Datenbank gespeichert und abgerufen
- Synchronisation zwischen DB, Logsystem und GUI ist zuverlässig
- Fehler und Inkonsistenzen werden sauber behandelt und angezeigt
- Isolation und Nachvollziehbarkeit bleiben auch bei parallelen und Multi-User-Szenarien erhalten

---

## Core-/venv-Tests: Health & Performance
- Test: Health-Check der App-Laufzeit in .venv_core (Startup, Ressourcen, Fehlerfreiheit)
- Test: Performance-Messung (Startzeit, CPU/RAM-Auslastung, Reaktionszeit)
- Test: PID-Erfassung und Logging für App-Prozesse
- Test: Fehlerhandling und Recovery bei Absturz oder Ressourcenengpässen
- Test: End-to-End-Test: App-Start → Health-Check → Performance-Messung → Logsystem/GUI

**Erfolgskriterien:**
- App läuft stabil und performant in .venv_core
- Health- und Performance-Daten werden korrekt erfasst und angezeigt
- Fehler und Engpässe werden sauber behandelt und geloggt

---

## venv_testbed-Tests: Health & Performance
- Test: Health-Check der Testumgebung (pytest, Integrationstests)
- Test: Performance-Messung für Testläufe (Dauer, Ressourcenverbrauch)
- Test: PID-Erfassung und Logging für Testprozesse
- Test: Fehlerhandling bei Testfehlschlägen oder Ressourcenproblemen
- Test: End-to-End-Test: Teststart → Health-Check → Performance-Messung → Logsystem/GUI

**Erfolgskriterien:**
- Testumgebung läuft stabil und performant
- Health- und Performance-Daten werden korrekt erfasst und angezeigt
- Fehler und Engpässe werden sauber behandelt und geloggt

---

## venv_selenium-Tests: Health & Performance
- Test: Health-Check für E2E-/Selenium-Tests (Browser, WebDriver)
- Test: Performance-Messung für UI-Tests (Laufzeit, Ressourcenverbrauch)
- Test: PID-Erfassung und Logging für Browser-/Testprozesse
- Test: Fehlerhandling bei Browser-/Testabsturz
- Test: End-to-End-Test: E2E-Teststart → Health-Check → Performance-Messung → Logsystem/GUI

**Erfolgskriterien:**
- E2E-/Selenium-Tests laufen stabil und performant
- Health- und Performance-Daten werden korrekt erfasst und angezeigt
- Fehler und Engpässe werden sauber behandelt und geloggt

---

## venv_build-Tests: Health & Performance
- Test: Health-Check für Build-Prozesse (pyinstaller, packaging)
- Test: Performance-Messung für Build-Läufe (Dauer, Ressourcenverbrauch)
- Test: PID-Erfassung und Logging für Buildprozesse
- Test: Fehlerhandling bei Buildfehlern oder Ressourcenproblemen
- Test: End-to-End-Test: Buildstart → Health-Check → Performance-Messung → Logsystem/GUI

**Erfolgskriterien:**
- Build-Prozesse laufen stabil und performant
- Health- und Performance-Daten werden korrekt erfasst und angezeigt
- Fehler und Engpässe werden sauber behandelt und geloggt

---

## venv_dev-Tests: Health & Performance
- Test: Health-Check für Entwicklungsumgebung (IDE, Linting, Debugging)
- Test: Performance-Messung für Dev-Tools (Laufzeit, Ressourcenverbrauch)
- Test: PID-Erfassung und Logging für Dev-Prozesse
- Test: Fehlerhandling bei Tool-Absturz oder Ressourcenproblemen
- Test: End-to-End-Test: Toolstart → Health-Check → Performance-Messung → Logsystem/GUI

**Erfolgskriterien:**
- Entwicklungsumgebung läuft stabil und performant
- Health- und Performance-Daten werden korrekt erfasst und angezeigt
- Fehler und Engpässe werden sauber behandelt und geloggt

---

## UI-Health-Tests
- Test: Health-Check der UI-Komponenten (Player, Playlist, Tab-Wechsel, Controls)
- Test: Performance-Messung für UI-Aktionen (Reaktionszeit, Rendering, Event-Handling)
- Test: PID-Erfassung und Logging für UI-Prozesse (Browser, WebView)
- Test: Fehlerhandling bei UI-Absturz, Hänger oder Rendering-Problemen
- Test: End-to-End-Test: UI-Start → Health-Check → Performance-Messung → Logsystem/GUI
- Test: Multi-User- und Multi-Tab-Szenarien (gleichzeitige UI-Aktionen, getrennte Sessions)

**Erfolgskriterien:**
- UI läuft stabil und performant
- Health- und Performance-Daten werden korrekt erfasst und angezeigt
- Fehler und Engpässe werden sauber behandelt und geloggt
- Synchronisation und Isolation bleiben auch bei parallelen und Multi-User-Szenarien erhalten

---

## Docker-Tests: Health & Performance
- Test: Health-Check für Docker-Container (Startup, Ressourcen, Fehlerfreiheit)
- Test: Performance-Messung für Container-Läufe (Startzeit, CPU/RAM-Auslastung, Netzwerk)
- Test: PID-Erfassung und Logging für Container-Prozesse
- Test: Fehlerhandling und Recovery bei Container-Absturz oder Ressourcenengpässen
- Test: End-to-End-Test: Container-Start → Health-Check → Performance-Messung → Logsystem/GUI

**Erfolgskriterien:**
- Container laufen stabil und performant
- Health- und Performance-Daten werden korrekt erfasst und angezeigt
- Fehler und Engpässe werden sauber behandelt und geloggt

---

## CLI-Tests: Health & Performance
- Test: Health-Check für CLI-Tools (cli.py, build_deb.sh, run.sh)
- Test: Performance-Messung für CLI-Befehle (Laufzeit, Ressourcenverbrauch)
- Test: PID-Erfassung und Logging für CLI-Prozesse
- Test: Fehlerhandling bei CLI-Absturz, Exit-Code, Ressourcenproblemen
- Test: End-to-End-Test: CLI-Start → Health-Check → Performance-Messung → Logsystem/GUI

**Erfolgskriterien:**
- CLI-Tools laufen stabil und performant
- Health- und Performance-Daten werden korrekt erfasst und angezeigt
- Fehler und Engpässe werden sauber behandelt und geloggt

---

## Smoke-Tests
- Test: Minimalstart aller Hauptkomponenten (App, Testbed, Selenium, Build, Dev, Docker, CLI)
- Test: PID-Erfassung und Logging für alle gestarteten Prozesse
- Test: GUI-Start und grundlegende UI-Aktionen (Tab-Wechsel, Player, Playlist)
- Test: CLI- und Docker-Befehle (run.sh, build_deb.sh, docker-compose)
- Test: Datenbank- und Parser-Pipeline-Start
- Test: Fehlerfreiheit beim Start (keine Exceptions, keine Crashs)
- Test: End-to-End-Test: Systemstart → Komponentenstart → PID-Logging → GUI/CLI/Docker

**Erfolgskriterien:**
- Alle Hauptkomponenten starten fehlerfrei und sind erreichbar
- PIDs werden korrekt erfasst und geloggt
- Keine Crashs oder kritischen Fehler beim Start
- Grundlegende Funktionen (UI, CLI, Docker, DB, Parser) laufen ohne Probleme

---

## Performance-Tests
- Test: Startzeit und Initialisierung aller Hauptkomponenten (App, Testbed, Selenium, Build, Dev, Docker, CLI)
- Test: CPU- und RAM-Auslastung während typischer Workflows (App-Betrieb, Testläufe, Build, Parser, DB, UI)
- Test: Reaktionszeit der UI (Tab-Wechsel, Player, Playlist, Controls)
- Test: Durchsatz und Laufzeit von Parser-Pipeline und Datenbankoperationen
- Test: Parallelbetrieb und Skalierung (gleichzeitige Prozesse, Multi-User, Multi-Tab)
- Test: Ressourcenengpässe und Fehlerhandling bei hoher Last
- Test: End-to-End-Test: Systemstart → Performance-Messung → Logsystem/GUI/Docker/CLI

**Erfolgskriterien:**
- Alle Komponenten laufen performant und skalierbar
- Performance-Daten werden korrekt erfasst und angezeigt
- Keine kritischen Engpässe oder Performance-Einbrüche
- Fehler und Ressourcenprobleme werden sauber behandelt und geloggt

---

## Anforderungen an die Test Suite

### Minimalanforderungen
- PID-Erfassung und Logging für alle Hauptprozesse (App, Testbed, Selenium, Build, Dev, Docker, CLI, Parser, DB)
- Fehlerfreier Start aller Komponenten (Smoke-Test)
- Grundlegende Health-Checks und UI-Funktionalität

### Pflichtanforderungen
- Performance-Messung und Ressourcenüberwachung für alle Workflows
- Synchronisation und Logging zwischen Backend, GUI, DB, Docker, CLI
- Fehlerhandling und Recovery bei Absturz, Ressourcenengpässen, DB-Fehlern
- End-to-End-Tests für alle Hauptprozesse und Workflows
- Multi-User- und Parallelbetrieb

### Maximalanforderungen
- Skalierbarkeit und Stress-Tests (viele Prozesse, Multi-Tab, Multi-User)
- Cross-Plattform-Kompatibilität (Linux, Windows, macOS, Docker)
- Audit-Trail und vollständige Nachvollziehbarkeit aller PID- und Prozessaktionen
- Integrationstests mit echter GUI-Kommunikation und API-Endpunkten
- Erweiterte Security- und Permission-Tests
- Automatisierte Regressionstests und kontinuierliche Überwachung

**Erfolgskriterien:**
- Alle Minimal- und Pflichtanforderungen sind erfüllt
- Maximalanforderungen können flexibel ergänzt werden
- Die Test Suite ist robust, skalierbar und praxisnah

---

### Optionale Anforderungen
- Erweiterte Monitoring- und Dashboard-Funktionen für PID, Performance und Health
- Visualisierung von Prozess- und Session-Flows (z.B. als Diagramm)
- Integration mit externen Monitoring- und Logging-Systemen (Prometheus, Grafana, ELK)
- Automatisierte Benachrichtigungen bei Fehlern, Engpässen oder kritischen Events
- Customizable Test-Szenarien und Parameter (z.B. für spezielle Workflows)
- Erweiterte Security-Checks (z.B. Sandbox, Rechteprüfung, Exploit-Tests)
- Historische Analyse und Reporting (Langzeit-Performance, Fehlerstatistik)
- Integration mit CI/CD-Pipelines für automatisierte Testausführung

**Hinweis:**
- Optionale Anforderungen können je nach Projektbedarf und Ressourcen flexibel ergänzt werden.

---

## Backend-Frontend-Sync-Tests
- Test: Synchronisation von PID, Status und Logs zwischen Backend und Frontend (GUI)
- Test: Echtzeit-Update der UI bei Prozessstart, -ende und Statusänderung im Backend
- Test: Fehlerhandling und UI-Feedback bei Backend-Problemen (z.B. Prozessabsturz, Timeout)
- Test: End-to-End-Test: Backend startet Prozess → PID und Status werden an Frontend übergeben → UI zeigt korrekte Infos
- Test: Multi-User- und Multi-Session-Szenarien (gleichzeitige Prozesse, getrennte Sessions)
- Test: Konsistenzprüfung: Backend- und Frontend-Daten stimmen überein (PID, Status, Logs)

**Erfolgskriterien:**
- Backend und Frontend sind synchronisiert und zeigen konsistente Daten
- UI reagiert zuverlässig auf Backend-Events und Fehler
- Synchronisation bleibt auch bei parallelen und Multi-User-Szenarien erhalten

---

## Keep-Alive- und Ping-Tests
- Test: Regelmäßiger Ping zwischen Backend und Frontend zur Verbindungsüberwachung
- Test: Keep-Alive-Mechanismus für Prozesse (App, Testbed, Selenium, Parser, DB, Docker, CLI)
- Test: UI-Feedback bei Verbindungsabbruch oder Timeout (z.B. Warnung, Reconnect)
- Test: End-to-End-Test: Prozess läuft → Ping/Keep-Alive → Status-Update in GUI/Logsystem
- Test: Fehlerhandling bei ausbleibendem Ping oder Keep-Alive (z.B. automatischer Neustart, Logging)
- Test: Multi-User- und Multi-Session-Szenarien (gleichzeitige Pings, getrennte Sessions)

**Erfolgskriterien:**
- Verbindungen und Prozesse werden zuverlässig überwacht
- UI und Logsystem reagieren auf Verbindungsstatus
- Keep-Alive und Ping funktionieren auch bei parallelen und Multi-User-Szenarien
- Fehler und Ausfälle werden sauber behandelt und angezeigt

---

## Build- und CI-Prozess-Tests
- Test: Health-Check und Performance-Messung für Build-Prozesse (pyinstaller, packaging, build_deb.sh)
- Test: PID-Erfassung und Logging für Build- und CI-Prozesse
- Test: Fehlerhandling bei Build-Fehlern, Exit-Codes, Ressourcenproblemen
- Test: End-to-End-Test: CI-Job startet Build → Health-Check → Performance-Messung → Logsystem/GUI
- Test: Synchronisation und Status-Update zwischen CI-System, Backend und Frontend
- Test: Multi-Job- und Parallelbetrieb (gleichzeitige Builds, mehrere CI-Jobs)
- Test: Audit-Trail und Nachvollziehbarkeit aller Build- und CI-Prozesse

**Erfolgskriterien:**
- Build- und CI-Prozesse laufen stabil und performant
- Health-, Performance- und PID-Daten werden korrekt erfasst und angezeigt
- Fehler und Engpässe werden sauber behandelt und geloggt
- Synchronisation und Nachvollziehbarkeit sind gewährleistet

---

## Prozessmanagement-Tests & Requirements
- Test: Start, Stop, Restart und Überwachung von Systemtools, Parsern, App, Testbed, Build, CI, Docker, CLI
- Test: PID-Erfassung, Status-Update und Logging für alle Prozessaktionen
- Test: Fehlerhandling bei unerwartetem Prozessende, Zombie-Prozessen, Ressourcenproblemen
- Test: Multi-User- und Multi-Session-Management (gleichzeitige Prozesse, getrennte Sessions)
- Test: End-to-End-Test: Prozessstart → Management (Stop/Restart) → Status-Update → Logsystem/GUI
- Test: Requirements-Check: Alle benötigten Tools, Libraries und Systemressourcen sind verfügbar und korrekt eingebunden
- Test: Automatisierte Prüfung der requirements.txt, environment.yml und Systemabhängigkeiten

**Erfolgskriterien:**
- Prozesse werden zuverlässig gemanagt und überwacht
- Alle Anforderungen (Tools, Libraries, Ressourcen) sind erfüllt und geprüft
- Fehler und Engpässe werden sauber behandelt und geloggt
- Multi-User- und Multi-Session-Management funktioniert robust

---

## E2E-Tests (End-to-End)
- Test: Gesamter Workflow von Datei-Upload bis Ergebnisanzeige in der GUI (inkl. Parser, DB, App, UI)
- Test: PID-Erfassung und Logging für alle beteiligten Prozesse (App, Parser, DB, UI, Docker, CLI)
- Test: Synchronisation und Status-Update zwischen Backend und Frontend während des gesamten Workflows
- Test: Fehlerhandling und Recovery bei Prozessabsturz, Timeout, Ressourcenproblemen
- Test: Multi-User- und Multi-Session-Szenarien (gleichzeitige E2E-Workflows, getrennte Sessions)
- Test: End-to-End-Test: Datei einlesen → Parser starten → PID erfassen → DB speichern → Ergebnis und PID in der GUI anzeigen
- Test: Audit-Trail und Nachvollziehbarkeit aller E2E-Prozesse

**Erfolgskriterien:**
- E2E-Workflows laufen stabil und performant
- PIDs und Status werden korrekt erfasst, synchronisiert und angezeigt
- Fehler und Engpässe werden sauber behandelt und geloggt
- Multi-User- und Multi-Session-Szenarien funktionieren robust
- Audit-Trail und Nachvollziehbarkeit sind gewährleistet

---

## Beispiel-Testfälle für E2E-Tests
1. Datei-Upload und Parser-Workflow:
   - Lade eine Mediendatei hoch
   - Starte Parser-Prozess (ffprobe, mutagen, mediainfo)
   - Erfasse und logge die PID
   - Speichere Ergebnis und PID in der Datenbank
   - Zeige Ergebnis und PID in der GUI an

2. Fehlerhandling bei Parser-Absturz:
   - Simuliere Parser-Absturz oder Timeout
   - Prüfe, ob Fehler im Logsystem und in der GUI angezeigt werden
   - Prüfe Recovery-Mechanismus

3. Multi-User-Workflow:
   - Starte mehrere Datei-Uploads und Parser-Prozesse parallel
   - Prüfe, ob PIDs, Ergebnisse und Sessions korrekt getrennt und angezeigt werden

4. End-to-End-Test für Build-Prozess:
   - Starte einen Build (pyinstaller, build_deb.sh)
   - Erfasse und logge die PID
   - Prüfe Status und Ergebnis in der GUI und im Logsystem

5. UI-Health-Test:
   - Starte die App-GUI
   - Führe Tab-Wechsel, Player- und Playlist-Aktionen aus
   - Prüfe Reaktionszeit, Fehlerfreiheit und PID-Logging

6. Docker-Integration:
   - Starte einen Docker-Container für App oder Testbed
   - Erfasse und logge die PID
   - Prüfe Status und Performance in der GUI und im Logsystem

**Erfolgskriterien:**
- Alle Testfälle laufen fehlerfrei und erfüllen die definierten Anforderungen
- PIDs, Status und Ergebnisse werden korrekt erfasst, synchronisiert und angezeigt
- Fehler und Engpässe werden sauber behandelt und geloggt

---

## CLI-Umgebung Tests
- Test: Health-Check und Performance-Messung für CLI-Tools (cli.py, run.sh, build_deb.sh)
- Test: PID-Erfassung und Logging für CLI-Prozesse
- Test: Fehlerhandling bei CLI-Absturz, Exit-Code, Ressourcenproblemen
- Test: End-to-End-Test: CLI-Start → Health-Check → Performance-Messung → Logsystem/GUI
- Test: Synchronisation und Status-Update zwischen CLI, Backend und Frontend
- Test: Multi-User- und Parallelbetrieb (gleichzeitige CLI-Befehle, mehrere Sessions)
- Test: Audit-Trail und Nachvollziehbarkeit aller CLI-Prozesse

**Erfolgskriterien:**
- CLI-Tools laufen stabil und performant
- Health-, Performance- und PID-Daten werden korrekt erfasst und angezeigt
- Fehler und Engpässe werden sauber behandelt und geloggt
- Synchronisation und Nachvollziehbarkeit sind gewährleistet
