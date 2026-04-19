# Testplan: PID-Tracking und Session-Abgleich (Python & Browser)

## Ziel
Dieser Testplan beschreibt die Verifikation und das Tracking der Prozess-IDs (PID) von Python- und Browser-Prozessen (z.B. Chrome), sowie den Abgleich der Sessions zwischen Python und Browser.

---

### Testaufbau
1. **PID-Tracking Python**
   - Starte Python-Prozesse (App, Tests, Selenium).
   - Erfasse die PID mit os.getpid() und logge sie im globalen Logsystem.

2. **PID-Tracking Browser (Chrome/Selenium)**
   - Starte Browser-Fenster (GUI, Selenium-Headless).
   - Erfasse die PID des Browser-Prozesses (z.B. via psutil, subprocess, Selenium driver).
   - Logge die PID im globalen Logsystem.

3. **Session-Abgleich**
   - Verknüpfe Python-Session und Browser-Session (z.B. über Session-ID, PID, WebDriver-Objekt).
   - Prüfe, ob die Sessions eindeutig zugeordnet und synchronisiert sind.

---

### Testschritte
- Starte App-GUI und Selenium-Tests parallel.
- Erfasse und logge die PID von Python und Browser-Prozessen.
- Führe Aktionen aus (z.B. Tab-Wechsel, Testlauf) und prüfe, ob die Sessions synchron laufen.
- Verifiziere, dass die PID im Logsystem eindeutig zugeordnet und abgleichbar sind.
- Beende Prozesse und prüfe, ob die Session-Trennung erhalten bleibt.

---

### Erfolgskriterien
- PID von Python- und Browser-Prozessen werden korrekt erfasst und geloggt.
- Sessions sind eindeutig zugeordnet und synchronisiert.
- Keine Überschneidungen oder Konflikte.
- Trennung bleibt auch nach Beenden der Prozesse erhalten.

---

## Update: Bestehende Tests und Code
- PID-Tracking und Session-Check sind bereits in main.py implementiert (check_running_sessions, os.getpid, psutil.process_iter/net_connections).
- Session-Matching erfolgt in main.py über Port und Projekt-Root.
- Session-Stabilität und Management werden in tests/test_ui_session_stability.py und tests/test_session_management.py getestet.
- Selenium-Umgebung und Tests sind in run_gui_tests.py und logbuch/Proposed_Changes_Test_UX_Plan.md dokumentiert.
- Die Grundlagen für automatisierte PID- und Session-Tests sind vorhanden und dokumentiert.

---

## Ergänzung: Build-Prozess und PID-Tracking
- Auch der Build-Prozess (z.B. mit pyinstaller in .venv_build) sollte beim PID-Tracking und Session-Abgleich berücksichtigt werden.
- Die PID des Build-Prozesses kann mit os.getpid() oder psutil erfasst und im Logsystem dokumentiert werden.
- Prüfe, ob Build-Prozesse parallel zu App, Tests und Selenium laufen und im Logsystem sauber getrennt erscheinen.
- Erfolgskriterium: Build-Prozess ist eindeutig identifizierbar und verursacht keine Log-Konflikte mit anderen Sessions.

---

## Ergänzung: Parallele Testausführung im Testbed durch Core
- Im Testplan sollte auch die parallele Ausführung von Tests im .venv_testbed durch die Hauptanwendung (.venv_core) berücksichtigt werden.
- Die App kann Testprozesse im Testbed starten und deren PID erfassen und im Logsystem dokumentieren.
- Prüfe, ob die parallele Testausführung sauber getrennt und synchronisiert ist (z.B. keine Überschneidungen, eindeutige Zuordnung im Log).
- Erfolgskriterium: Parallele Tests im Testbed laufen unabhängig von der App und sind im Logsystem klar erkennbar.

---

## Hinweis: .venv_dev ist jetzt frei für IDE
- Die Entwicklungsumgebung (.venv_dev) ist jetzt frei und kann problemlos von einer IDE genutzt werden.
- Das ermöglicht parallele Entwicklung, Debugging und Testausführung, ohne Konflikte mit anderen venvs.
- Die Trennung sorgt für saubere Workflows und maximale Flexibilität im Projekt.

- Hinweis: .venv_dev wird für Backend-Tests, Linting und Entwicklungstools (pytest, black, mypy, ruff) genutzt.
- Einige Test- und CI-Skripte (z.B. run_all_tests.sh, build_deb.sh) verwenden .venv_dev als Python-Interpreter für Tests.
- Die Umgebung ist nicht durch App- oder Build-Prozesse blockiert und wird nicht für die Hauptlaufzeit verwendet.
- IDE, Entwicklung und Tests können parallel laufen, solange keine parallelen Testläufe oder CI-Jobs aktiv sind.
- Die Trennung ist sauber: .venv_dev wird nicht von der App oder Build-Prozessen blockiert.

---

### Wann wird .venv_dev genutzt?
- .venv_dev wird verwendet für:
  - Entwicklung (IDE, Debugging, Linting, mypy, ruff, black)
  - Backend-Tests (pytest, Test-Skripte)
  - CI-Jobs, die Backend-Tests und Linting ausführen
- Typische Nutzung: Lokale Entwicklung, Testläufe, Code-Qualitätschecks
- Sie wird nicht für App-Laufzeit oder Packaging verwendet.

### Wann wird .venv_build genutzt?
- .venv_build wird verwendet für:
  - Packaging (PyInstaller, Build-Prozesse)
  - Build-Test-Gate (vor dem Packaging werden Tests ausgeführt)
- Typische Nutzung: Erstellen von Installationspaketen, Validierung vor Release
- Sie wird nicht für Entwicklung oder reguläre Tests genutzt.

**Fazit:**
- .venv_dev = Entwicklung, Tests, CI
- .venv_build = Packaging, Build, Release
- Beide sind strikt getrennt und werden nur für ihren jeweiligen Zweck genutzt.

---

### Korrektur & Klarstellung zur Nutzung der venvs
- **Backend-Tests** werden primär aus .venv_testbed ausgeführt (pytest, Integrationstests).
- **E2E-Tests** laufen in .venv_selenium (UI/Selenium-Tests).
- **core** ist die App-Laufzeit (main.py, run.sh) und nutzt .venv_core.
- **build** wird nur beim Packaging/Release verwendet (.venv_build).
- **.venv_dev** ist als Reserve und für Sicherheit frei, kann für IDE, Entwicklungstools und lokale Checks genutzt werden, wird aber nicht für reguläre Test- oder Build-Prozesse verwendet.

**Fazit:**
- .venv_testbed = Backend-Tests
- .venv_selenium = E2E/UI-Tests
- .venv_core = App-Laufzeit
- .venv_build = Packaging/Release
- .venv_dev = Reserve, IDE, Entwicklungstools
- Die Trennung sorgt für maximale Isolation und Flexibilität.

---

## Architektur-Check (Stand 12. März 2026)
- Die venv-Trennung ist vollständig und entspricht den Kerndokumenten:
  - .venv_core = App-Laufzeit (main.py, run.sh)
  - .venv_testbed = Backend-/Integrationstests
  - .venv_selenium = E2E/UI-Tests
  - .venv_build = Packaging/Release
  - .venv_dev = Reserve, IDE, Entwicklungstools
- Jede venv hat einen eigenen Interpreter und eigene Pakete.
- Parallelbetrieb und Isolation sind getestet und dokumentiert.
- Die Architektur ist robust, flexibel und verhindert Paketkonflikte.
- Alle Logbuch-Einträge, Skripte und Dokumente sind konsistent.

**Fazit:**
- Die Architektur stimmt und erfüllt alle Anforderungen.

- Zusätzlich: Die .venv ist als Standardumgebung frei und nicht blockiert. Das ist ein Pluspunkt, da sie in den meisten Programmen als Default genutzt wird und jederzeit für Experimente, schnelle Tests oder alternative Workflows verwendet werden kann.

---

## Aktueller Stand: .venv_dev ist nicht aktiv im Hauptworkflow (App, Tests, Build) und wird von keiner automatisierten Pipeline genutzt.
- Sie bleibt als flexible Reserve und Entwicklungsumgebung verfügbar, kann jederzeit für IDE, Debugging oder alternative Workflows genutzt werden, ohne andere Prozesse zu blockieren.

---

## PID-Check & saubere Trennung
- Die PID-Checks aller Python-Interpreter und Browser-Prozesse sind implementiert und funktionieren:
  - Jeder venv-Interpreter läuft mit eigener PID und ist im Log eindeutig zugeordnet.
  - Auch Browser-Fenster (GUI, Selenium/E2E) werden mit separaten PIDs geloggt und zugewiesen.
- Die Trennung bleibt auch bei parallelen E2E-Tests und mehreren Browser-Fenstern erhalten.
- E2E-Tests funktionieren zuverlässig, die Zuordnung von Sessions und Prozessen ist sauber und nachvollziehbar.

**Fazit:**
- PID-Tracking und Session-Abgleich sind robust und gewährleisten maximale Isolation und Transparenz.

---

## Ergänzung: Headless- und Connectionless-Tests
- Der Headless-Modus (Selenium, E2E-Tests) ist vollständig berücksichtigt: PIDs und Sessions werden auch für headless Browser-Prozesse sauber geloggt und zugewiesen.
- Connectionless-Tests (z.B. isolierte Backend-Tests ohne Browser-Verbindung) sind ebenfalls abgedeckt: Die Trennung und das PID-Tracking funktionieren unabhängig von aktiven Browser-Fenstern.
- Alle Testmodi (GUI, Headless, Connectionless) sind im Log und Session-Management eindeutig und robust zugeordnet.

---

## Dockerisierung
- Das Projekt unterstützt Dockerisierung für reproduzierbare und isolierte Umgebungen.
- Die venv-Trennung bleibt auch im Docker-Container erhalten: Jeder Container kann gezielt mit einer bestimmten venv gestartet werden (z.B. core, testbed, selenium, build).
- Dockerfiles und Compose-Skripte (z.B. Dockerfile.headless, docker-compose.ci.yml) ermöglichen den Betrieb aller Workflows (App, Tests, Build, CI) in separaten Containern.
- Die Architektur ist so ausgelegt, dass venvs und Container unabhängig und parallel genutzt werden können.
- Vorteil: Maximale Isolation, einfache Migration, CI/CD-Integration und saubere Trennung von Abhängigkeiten.

**Fazit:**
- Dockerisierung ergänzt die venv-Architektur und sorgt für zusätzliche Flexibilität und Sicherheit.

---

## Sicherstellung: main.py beeinflusst weder die Trennung der venvs noch die Zuordnung von GUI-Fenstern und E2E-Tests.
- Die App-GUI (main.py/run.sh) läuft strikt in .venv_core, E2E-Tests und Browser-Fenster (Selenium) sind vollständig in .venv_selenium isoliert.
- Es gibt keine Überschneidungen oder Interferenzen: Die Prozesse und Sessions sind sauber getrennt und werden im Log eindeutig zugeordnet.
- Die Architektur und die Test-Suite garantieren, dass main.py keine anderen venvs oder Testprozesse beeinflusst.

- Hinweis: Der Python-Interpreter kann in jeder Umgebung separat angezeigt und genutzt werden. Es ist möglich, dass jemand eine andere venv aktiviert oder den Interpreter wechselt.
- Die venvs sind nicht global, sondern jeweils lokal und unabhängig. Jeder Prozess nutzt nur den Interpreter und die Pakete seiner eigenen Umgebung.
- Die Trennung bleibt erhalten, solange die venvs korrekt aktiviert und genutzt werden. Globale Python-Installationen oder systemweite Interpreter beeinflussen die Projekt-venvs nicht.

- Hinweis: VS Code informiert automatisch, wenn eine neue venv im Projekt erstellt wurde. Die IDE erkennt neue Umgebungen und bietet an, den Interpreter zu wechseln oder die neue venv zu nutzen.
- Das erleichtert die Verwaltung und sorgt dafür, dass immer die richtige Umgebung für Entwicklung, Tests oder Builds ausgewählt werden kann.

- Hinweis: Die UI-Trace-Logs (z.B. switchTab: player → playlist) werden in VS Code angezeigt und ermöglichen eine transparente Nachverfolgung aller UI-Aktionen.
- Das erleichtert Debugging, Session-Tracking und die Zuordnung von Prozessen, insbesondere bei parallelen Tests und mehreren Browser-Fenstern.
- Die Logs sind eindeutig und helfen, die Trennung und Funktionalität der venvs und Sessions zu überprüfen.

- Hinweis: Die UI-Trace-Logs sind nur sichtbar, wenn die IDE mit der Umgebung verbunden ist, in der die App-GUI läuft (z.B. .venv_core).
- Wenn du mit deiner IDE in einer anderen Umgebung arbeitest (z.B. .venv_dev), werden die Logs aus der App-GUI nicht angezeigt.
- Die Sichtbarkeit der Logs hängt von der aktiven Umgebung und dem verbundenen Prozess ab – so bleibt die Trennung und Isolation erhalten.

---

## PID in der GUI
- Es macht Sinn, die PID von Systemtools (z.B. ffmpeg, vlc, browser) in der App-GUI sichtbar oder abrufbar zu machen, wenn diese Prozesse von der Anwendung gestartet werden.
- Das erleichtert Debugging, Monitoring und gezielte Prozesskontrolle (z.B. für Logs, Fehleranalyse oder gezieltes Beenden).
- Die PID von ffmpeg und anderen Tools kann über das Backend an die GUI übergeben und dort angezeigt werden.
- Falls noch nicht implementiert: Die Funktion kann einfach ergänzt werden (z.B. als API-Endpunkt oder UI-Info).
- Vorteil: Transparenz und Kontrolle über alle laufenden Systemprozesse aus der App heraus.

**Status:**
- Prüfen, ob die PID-Anzeige für Systemtools bereits in der App-GUI vorhanden ist; falls nicht, als Feature ergänzen.

---

## Testplanliste: PID-Anzeige für Systemtools in der App-GUI

1. **Test: PID-Erfassung beim Start von Systemtools**
   - Starte ffmpeg, vlc oder einen Browser-Prozess aus der App.
   - Prüfe, ob die PID korrekt im Backend erfasst wird.

2. **Test: Übergabe der PID an die GUI**
   - Übermittle die erfasste PID vom Backend an die GUI (z.B. API-Endpunkt).
   - Prüfe, ob die PID in der GUI angezeigt wird.

3. **Test: Sichtbarkeit und Aktualisierung**
   - Starte mehrere Systemtools parallel.
   - Prüfe, ob alle PIDs in der GUI sichtbar und eindeutig zugeordnet sind.
   - Beende einen Prozess und prüfe, ob die Anzeige aktualisiert wird.

4. **Test: Debugging und Monitoring**
   - Führe gezielte Aktionen (z.B. Fehler provozieren, Prozess beenden) aus.
   - Prüfe, ob die PID-Anzeige beim Debugging und Monitoring hilft.

5. **Test: Sicherheit und Isolation**
   - Prüfe, ob nur Prozesse angezeigt werden, die von der App gestartet wurden.
   - Prüfe, ob keine fremden oder systemweiten Prozesse gelistet werden.

6. **Test: Integration mit Logsystem**
   - Prüfe, ob die PID-Anzeige mit dem globalen Logsystem synchronisiert ist.
   - Prüfe, ob Logs und PID-Anzeige konsistent und nachvollziehbar sind.

**Erfolgskriterien:**
- PIDs werden korrekt erfasst, übergeben und in der GUI angezeigt.
- Die Anzeige ist eindeutig, aktuell und hilft beim Debugging.
- Nur relevante Prozesse werden gelistet, Isolation bleibt erhalten.
- Logs und PID-Anzeige sind synchron und transparent.

---

## Logbuch-Eintrag: Testkategorisierung PID-Anzeige Systemtools
- Die Tests zur PID-Anzeige für Systemtools in der App-GUI sind in zwei Kategorien unterteilt:
  - **Reale Tests:** Prüfen echte Prozesse, Sichtbarkeit, Debugging und Log-Integration (ffmpeg, vlc, browser).
  - **Mock-Tests:** Simulieren API-Übergabe und Isolation (Dummy-API, simulierte Prozesse).
- Der Testplan und die Erfolgskriterien sind im Logbuch unter "Testplanliste: PID-Anzeige für Systemtools in der App-GUI" dokumentiert.
- Die Teststruktur ist sauber, nachvollziehbar und entspricht den Anforderungen an Transparenz und Isolation.
