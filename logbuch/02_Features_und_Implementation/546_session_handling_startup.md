# Logbuch: Session-Handling & Startup-Logik (2026-03-15)

**Datum:** 2026-03-15

## Ablauf & Verhalten
- Beim Start prüft das Backend, ob bereits eine laufende Session (Prozess/Port) existiert.
- Falls ja, wird **kein neuer Browser** und **keine neue App-Instanz** gestartet.
- Stattdessen wird die bestehende Session (inkl. URL und PID) erkannt und übernommen.
- Die Datenbank wird initialisiert, aber keine redundanten Ressourcen werden geöffnet.
- Der Browser wird im App-Modus gestartet und auf die bestehende Session-URL umgeleitet.

## Log-Auszug (Beispiel)
```
2026-03-15 19:57:44 [INFO] [root] [Startup] Command: $ .../python .../main.py
2026-03-15 19:57:44 [INFO] [root] [Startup] Database initialized: .../database.db
2026-03-15 19:57:45 [WARNING] [root] [Session] Existing session detected (PID 1782281, port 46503). Skipping new window launch.
2026-03-15 19:57:45 [INFO] [root] [Session] Existing session URL: http://localhost:46503/app.html
2026-03-15 19:57:45 [INFO] [root] [Browser] Launching chromium in app mode
2026-03-15 19:57:45 [INFO] [root] [Session] Opened existing session URL.
```

## Ergebnis
- **Keine Doppel-Instanzen**: Parallele Starts führen nicht zu mehreren Fenstern oder konkurrierenden Prozessen.
- **Ressourcenschonend**: Bereits laufende Sessions werden erkannt und genutzt.
- **Robustheit**: Die Anwendung bleibt stabil und benutzerfreundlich, auch bei versehentlichem Mehrfachstart.

---

*Letzte Änderung: 2026-03-15*
