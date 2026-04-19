# Erweiterter Implementation Plan – GUI, Backend & RTT/Data Flow

## Ziel
Behebung und Erweiterung folgender Punkte:
- AssertionError durch doppeltes `@eel.expose` (bereits erledigt)
- Chrome-Startparameter/Headless-Probleme
- Broken Tabs (Parser, Debug, Test, Reporting) durch DIV/Ungleichgewicht und WebSocket/UTF-8-Fehler
- Items werden im GUI nicht geladen (DB/Sync)
- **Neu:** RTT- (Round Trip Time) Test und Data-Flow-Dokumentation

---

## Backend Core
### Änderungen in `main.py`
- [x] **Redundantes `@eel.expose` entfernen** (bereits erledigt)
- [NEW] **RTT und Synchronisation:**
  - `rtt_ping(data)`: Loggt Empfang von Daten (dict, dict of dict, list of dicts), gibt 'pong' zurück
  - `confirm_receipt(event_name)`: Loggt, dass das Frontend Daten empfangen und verarbeitet hat
  - `sanitize_json(data)`: Hilfsfunktion, um alle Strings vor Eel-Transfer auf UTF-8 zu prüfen
- [NEW] **Automatisierter RTT-Test:**
  - `tests/test_rtt.py`: Script zur Überprüfung des RTT-Zyklus und der Datenintegrität

---

## Frontend
### Änderungen in `app.html`
- [x] **DIV-Ungleichgewicht in Options/Reporting behoben**
- [NEW] **RTT-Test-Integration:**
  - `runRTTTest()`: Sendet Testdaten an `rtt_ping`, wartet auf Antwort, ruft `confirm_receipt` auf, zeigt Timing und Datenstufen im UI/Console
  - **Button "Run RTT Test"** im Debug-Tab (oder Options-Tab)
- [NEW] **Data-Flow-Doku:**
  - Dokumentation des Datenflusses (dict → sql → json) im Logbuch und/oder UI

---

## Nützlicher Befehl: DIV-Balance an Schlüsselstellen prüfen

```bash
python3 -c "
import re
points = [3150, 3500, 3630, 3920, 4000, 4100, 4150, 4420]
with open('web/app.html', 'r') as f:
    balance = 0
    for i, line in enumerate(f, 1):
        balance += len(re.findall('<div', line)) - len(re.findall('</div', line))
        if i in points:
            print(f'Line {i}: Balance = {balance}')
"
```

Mit diesem Befehl kann an definierten Zeilen die aktuelle <div>-Balance in der app.html geprüft werden. Das hilft, Strukturfehler gezielt zu lokalisieren und zu beheben.

---

## Nützlicher Befehl: Kontextsuche für tab-content

```bash
grep -nC 10 "tab-content" web/app.html | head -n 20
```

Mit diesem Befehl werden die ersten 20 Zeilen Kontext rund um Vorkommen von 'tab-content' in der app.html angezeigt. Das hilft, die Einbettung und Struktur der Tab-Container schnell zu überprüfen.

---

## Nützlicher Befehl: Segmentweise <div>-Balance prüfen

```bash
for seg in "1-3151" "3152-3921" "3922-4421" "4422-5118" "5119-10943"; do
    start=${seg%-*}
    end=${seg#*-}
    opens=$(sed -n "${start},${end}p" web/app.html | grep -o "<div" | wc -l)
    closes=$(sed -n "${start},${end}p" web/app.html | grep -o "</div" | wc -l)
    echo "Segment $seg: Opens=$opens, Closes=$closes, Delta=$((opens - closes))"
done
```

Mit diesem Shell-Skript kann die Anzahl der geöffneten und geschlossenen <div>-Tags in beliebigen Segmenten der app.html gezählt werden. Das hilft, strukturelle Fehler gezielt einzugrenzen.

---

## Nützlicher Befehl: Logbuch-Tab/Panel schnell finden

```bash
grep -nC 5 "/localized-markdown-documentation-journal-panel" web/app.html || \
  grep -nC 5 "LOGBUCH TAB END" web/app.html
```

Mit diesem Befehl kann der Bereich des Logbuch-Tabs bzw. der zugehörigen Panel-Komponente in der app.html schnell lokalisiert werden – inklusive 5 Zeilen Kontext.

---

## Nützlicher Link: Lokale HTML-Vorschau

- [http://localhost:8345/app.html](http://localhost:8345/app.html)

Mit diesem Link kann die aktuelle app.html direkt im Browser betrachtet werden (z.B. für manuelle Struktur- und GUI-Checks während der Entwicklung oder nach Fixes).

---

## Verification Plan

### Automatisierte Tests
- **Neue Datei:** `tests/test_backend_api.py`
  - Teste, dass `eel.get_library()` Items liefert, wenn die DB nicht leer ist
  - Teste, dass `eel.scan_media()` ein Testverzeichnis erfolgreich indiziert
- **Neue Datei:** `tests/test_rtt.py`
  - Teste RTT-Zyklus und Datenintegrität
- **Testausführung:**
  ```bash
  pytest tests/test_backend_api.py
  pytest tests/test_rtt.py
  ```

### Manuelle Verifikation
- **App starten:**
  ```bash
  ./run.sh
  ```
- **Checkliste:**
  - Kein AssertionError beim Start
  - Chrome öffnet mit Fenstergröße 1550x800
  - Parser-, Debug-, Tests- und Reporting-Tabs sind sichtbar, klickbar und zeigen Daten (UTF-8-Fehler gelöst)
  - Items werden in Library- und Player-Tab geladen und angezeigt
  - RTT-Test-Button bestätigt Synchronisation mit < 100ms Latenz
  - Data-Flow-Doku (dict → sql → json) ist im Logbuch/UI verfügbar

---

**Hinweis:**
Nach Umsetzung und Test bitte Logbuch-Eintrag ergänzen und ggf. weitere Regressionstests anstoßen.
