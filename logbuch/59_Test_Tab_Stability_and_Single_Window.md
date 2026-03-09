<!-- Category: BUG -->
<!-- Status: COMPLETED -->

# Test-Tab Stabilität & Doppel-Fenster-Schutz

## Problem
Beim Ausführen von Tests im `Tests`-Tab trat ein instabiles Verhalten auf:
- Testausgabe erschien nur kurz.
- UI sprang danach zurück in den `Player`-Tab.
- Teilweise wirkte es so, als würde die Session neu starten bzw. ein zweites Fenster beteiligt sein.

## Root Cause
Über Live-Trace wurde sichtbar:
- Es kam zu echten Browser-Unload-Events (`beforeunload`, `pagehide`, `unload`).
- Im Eel-Keepalive-Pfad wurde dadurch ein `SystemExit` ausgelöst.
- Dadurch endete die Session und die UI erschien im Startzustand (Player-Tab).
- Zusätzlich wurde ein Doppel-Launch-Risiko identifiziert: `eel.start(...)` lief nicht explizit im `mode=False` und konnte in der installierten Eel-Version einen automatischen Browser-Start triggern, während parallel manuell Chromium per `subprocess.Popen(...)` gestartet wurde.
- Finaler Auslöser für das weiterhin auftretende Zweitfenster: Einige Tests triggern intern den connectionless-Pfad (`run_connectionless_browser_mode()`), der ein Offline-Fenster (`file:///.../web/app.html`) öffnen kann.

## Umsetzung
### Backend (`main.py`)
- `run_tests(...)` entkoppelt (Worker-Thread + wait-loop mit `time.sleep`) damit der Eel-Loop nicht blockiert.
- Test-Output serverseitig begrenzt, um große Payloads/Disconnects zu vermeiden.
- Pytest-Ausgabe auf `-q` reduziert.
- Testprozess mit Timeout abgesichert (`subprocess.run(..., timeout=900)`).
- Ergebnis-Parsing für `pytest -q` robust gemacht (`passed/failed`-Erkennung korrigiert).
- Keepalive-Härtung: `BaseException` im Loop abgefangen (außer `KeyboardInterrupt`), damit Unload-bedingte `SystemExit`-Ereignisse die App nicht beenden.
- Neuer Eel-Endpunkt `ui_trace(...)` für Frontend→Backend Trace-Logging im Terminal.
- `eel.start(...)` auf `mode=False` gestellt, damit **kein** automatischer Eel-Browserstart erfolgt und nur der manuelle Chromium-App-Launch aktiv bleibt (Single-Window-Quelle).
- Mehrfachinstanz-Guard ergänzt: Bei bereits laufender Session wird kein neues Fenster mehr gestartet.
- Browser-Open-Seiteneffekte während UI-Testläufen unterdrückt: `run_tests(...)` setzt `MWV_DISABLE_BROWSER_OPEN=1`, `run_connectionless_browser_mode()` respektiert den Flag.

### Frontend (`web/app.html` + Packaging-Spiegel)
- Test-Output robuster (vertikales Scrolling, Zeilenumbruch, große Ausgabe abgeschnitten).
- Re-Entry-Schutz beim Teststart (`isTestRunInProgress`) + Run-Button Disable/Enable gegen Mehrfachklicks.
- Starttext i18n-basiert (`test_run_starting`) statt hart codiert.
- Live-Trace integriert für:
  - Tabwechsel
  - Reload/Unload-Events
  - Connection-State-Übergänge
  - JS Errors/Unhandled Rejections
- Trace wird zusätzlich ins Backend-Log weitergeleitet.

## Tests
Neue Regression-Testdatei:
- `tests/test_ui_session_stability.py`

Abgedeckte Checks:
1. Keepalive fängt `BaseException/SystemExit` ab.
2. Nur eine Browser-Launch-`subprocess.Popen`-Stelle im Startup-Pfad.
3. UI-Trace-Bridge (`eel.ui_trace`) vorhanden.
4. Re-Entry-Schutz für `runSelectedTests()` aktiv.
5. `eel.start("app.html", mode=False, ...)` als Schutz gegen Doppel-Fenster erzwungen.
6. Existing-Session-Guard verhindert zweites Fenster beim erneuten Start.
7. Browser-Open-Suppression (`MWV_DISABLE_BROWSER_OPEN`) für UI-Test-Subprozesse aktiv.

Ergebnis:
- `python -m pytest tests/test_ui_session_stability.py -q`
- **6 passed**

## Ergebnis
Der bekannte Sprung aus dem `Tests`-Tab in den `Player` durch Session-Abbruch wurde technisch abgesichert und reproduzierbar dokumentiert. Die Regression ist jetzt testbar und dauerhaft über die Test-Suite abgedeckt.
