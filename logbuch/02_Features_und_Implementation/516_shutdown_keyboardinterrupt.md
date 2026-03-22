# Beenden des Programms per IDE-Stop/KeyboardInterrupt

**Datum:** 15.03.2026

## Übersicht
Dieses Logbuch beschreibt das Verhalten der Anwendung beim Beenden über die IDE (Stop-Button) bzw. durch KeyboardInterrupt (z.B. Strg+C).

---

## 1. Ablauf beim Beenden
- Im Hauptloop (`src/core/main.py`) wird `eel.sleep(1.0)` in einer Endlosschleife ausgeführt.
- Ein KeyboardInterrupt (z.B. durch Stop in der IDE) wird per `except KeyboardInterrupt` abgefangen:
  ```python
  while True:
      try:
          eel.sleep(1.0)
      except KeyboardInterrupt:
          logging.info("[Shutdown] KeyboardInterrupt received. Exiting.")
          raise
      except BaseException as e:
          logging.warning(f"[WebSocket] keepalive recovered from base error: {type(e).__name__}: {e}")
          time.sleep(1.0)
  ```
- Nach dem Loggen der Shutdown-Info wird die Exception erneut ausgelöst (`raise`), wodurch das Backend sofort beendet wird.

---

## 2. Ressourcenbereinigung
- Es gibt **keinen expliziten Cleanup** für gestartete Subprozesse (z.B. Browser), offene Dateien oder andere Ressourcen.
- Der Browser-Prozess, der beim Starten der Anwendung geöffnet wurde, bleibt nach dem Beenden des Backends ggf. weiter aktiv.
- Ein automatisches Beenden des Browsers beim Stoppen des Backends ist aktuell **nicht implementiert**.

---

## 3. Hinweise & Empfehlungen
- Für ein vollständiges, sauberes Beenden sollten beim Shutdown alle gestarteten Subprozesse (z.B. Browser) explizit terminiert werden (z.B. per `os.kill(BROWSER_PID, signal.SIGTERM)` oder `process.terminate()`).
- Das aktuelle Verhalten ist für reine Backend-Prozesse ausreichend, aber für Desktop-Apps mit Subprozessen sollte Cleanup ergänzt werden.

---

**Siehe auch:**
- [Browser PID und Auswahl – Logbuch](2026-03-15_browser_pid_und_auswahl.md)
- [Debugging-Strategien – Logbuch](2026-03-15_fenster_schliesst_debugging.md)
