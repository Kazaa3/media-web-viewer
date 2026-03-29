# Browser PID und Auswahl – Logbuch

**Datum:** 15.03.2026

## Übersicht
Dieses Logbuch dokumentiert, wie und wo im System die PID (Process ID) des gestarteten Browsers sowie die Auswahl des verwendeten Browsers (Chrome, Chromium, Firefox etc.) erfasst und geloggt werden.

---

## 1. Erfassung der Browser-PID
- Die globale Variable `BROWSER_PID` wird in `src/core/main.py` deklariert und beim Starten des Browsers gesetzt:
  - **Deklaration:**
    ```python
    BROWSER_PID = None  # Global to track browser process
    ```
  - **Setzen der PID:**
    ```python
    process = subprocess.Popen([...])
    global BROWSER_PID
    BROWSER_PID = process.pid
    ```
  - Die PID wird gesetzt, wenn der Browser im App-Mode (z.B. Chromium) direkt per `subprocess.Popen` gestartet wird.

- **Frontend-Anzeige:**
  - Die PID wird im Frontend (web/app.html) angezeigt:
    ```html
    <div><b>Browser PID:</b> <span id="debug-browser-pid" style="color: #6a1;">-</span>
    ```

---

## 2. Auswahl des Browsers
- Die Auswahl des Browsers erfolgt in `src/core/main.py`:
  - Es werden verschiedene Kandidaten geprüft (z.B. `google-chrome`, `chromium-browser`, `firefox`).
  - Die Auswahl wird geloggt:
    ```python
    logging.info(f"[Browser] Selected: {browser_name} ({browser_path})")
    ```
  - Die Variable `browser_name` enthält den Namen des gewählten Browsers.

- **Frontend-Anzeige:**
  - Im Frontend werden Name, Pfad und Version des Browsers angezeigt:
    ```js
    const browserName = toolsStatus.browser_name || 'browser';
    const browserPath = toolsStatus.browser_path || '';
    const browserVer = toolsStatus.browser_version || '';
    ```

---

## 3. Zusammenfassung
- Die PID des gestarteten Browsers und die Auswahl (Name/Pfad/Version) werden sowohl im Backend geloggt als auch im Frontend angezeigt.
- Die Implementierung ist in `src/core/main.py` (Backend) und `web/app.html`/`web/script.js` (Frontend) zu finden.

---

**Siehe auch:**
- [PID-Logging und Anzeige – Logbuch](2026-03-15_pid_logging_anzeige.md)
- [Debugging-Strategien – Logbuch](2026-03-15_fenster_schliesst_debugging.md)
