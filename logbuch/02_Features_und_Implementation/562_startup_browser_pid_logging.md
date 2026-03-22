# Logbuch: Startup-Logging – Browser PID beim Start erfassen (2026-03-15)

**Datum:** 2026-03-15

## Änderung
- Beim Start der Anwendung wird jetzt zusätzlich zur Python- und Session-PID auch die **Browser-PID** (z.B. Chromium) im Log erfasst und ausgegeben.
- Beispiel-Logauszug:
```
2026-03-15 21:34:56 [INFO] [root] [Startup] Command: $ .../python .../main.py
2026-03-15 21:34:56 [INFO] [root] [Startup] Database initialized: .../database.db
2026-03-15 21:34:56 [WARNING] [root] [Session] Existing session detected (PID 1837179, port 32815). Skipping new window launch.
2026-03-15 21:34:56 [INFO] [root] [Session] Existing session URL: http://localhost:32815/app.html
2026-03-15 21:34:56 [INFO] [root] [Browser] Launching chromium in app mode
2026-03-15 21:34:56 [INFO] [root] [Browser] Chromium PID: 1837201  # <--- Browser-PID wird jetzt explizit geloggt
2026-03-15 21:34:56 [INFO] [root] [Session] Opened existing session URL.
```

## Vorteile
- Bessere Nachvollziehbarkeit und Debugging bei mehreren gleichzeitigen Sessions oder Browser-Instanzen.
- Ermöglicht gezieltes Monitoring und Troubleshooting (z.B. bei Zombie-Prozessen oder Browser-Crashes).

## Umsetzung
- Die PID des gestarteten Browsers wird direkt nach dem Launch im Log ausgegeben.
- Bei bestehenden Sessions kann die PID aus der Session-Verwaltung oder dem Prozessbaum ermittelt werden.

---

*Letzte Änderung: 2026-03-15*
