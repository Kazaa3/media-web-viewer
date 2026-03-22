# 14 Status-Bericht: GUI-Test-Suite & Picking-Problematik

Datum: 2026-03-11
Status: In Arbeit / Instabil

## Aktueller Stand
Wir haben eine industrielle Test-Suite auf Basis von Selenium aufgebaut (`.venv_selenium`). Trotz technischer Fixes (Umstellung auf `mousedown`/`mouseup`) bleibt das Verhalten für den User unzuverlässig ("Picking funktioniert für mich immer noch nicht").

## Analyse der Test-Suite (Stand 19:00 Uhr)
Der letzte Suite-Lauf zeigt eine kritische Diskrepanz:
- **Technischer Erfolg**: Die Logs zeigen `[UI-Trace] Picked item 0`. Das Event wird also im DOM getriggert.
- **Funktionaler Fehler**: Im `test_scenario_hammerhart` schlug die Assertion fehl. Der Song wurde nicht an die Zielposition verschoben, sondern blieb an Index 0.
- **Problemquelle**: Möglicherweise wird der state-sync durch den massiven Hintergrund-Scan (Parser) verzögert oder blockiert.

## Bekannte Probleme & Bottlenecks
1. **Parser-Last**: Der Scanner produziert Hunderte von Fehlern (`[Errno 21] Is a directory`), was die Event-Loop belasten könnte.
2. **Timing & Timeouts**: Viele Tests leiden unter `TimeoutException`, da die UI während des initialen Scans zu träge reagiert.
3. **Startup-Performance**: Die Zeit vom Programmstart bis zur UI-Bereitschaft ist aktuell nicht quantifizierbar.

## Nächste Schritte (Systematische Aufarbeitung)
1. **Telemetrie**: Einführung von "Parser Begin" und "Parser End" Logs in Python, um die Lastphasen exakt zu identifizieren.
2. **Startup-Optimierung**: Zeitmessung der Startphase (`main.py`).
3. **Picking-Deep-Dive**: Debugging der JavaScript-Funktion `move_item_to` und deren Rückwirkung auf `renderPlaylist`. Warum "wandert" das Item im DOM nicht weiter, obwohl der Pick registriert wurde?
4. **Scanner-Fix**: Verzeichnisse im Medien-Scanner explizit überspringen, um Fehler-Rauschen und Retries zu minimieren.
