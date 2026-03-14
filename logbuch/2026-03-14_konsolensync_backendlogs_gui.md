# Konsolen-Synchronisation: Fehlende Backend-Logs in der GUI

**Datum:** 14.03.2026

## Problem
- In der GUI-Konsole erscheinen aktuell nur UI-Traces (z. B. `switchTab`, `sync-state`), aber nicht die vollständigen Backend-Logs (Startup, Environment, Datenbank, Session, Browser-Start etc.), wie sie im Terminal ausgegeben werden.

## Erwartetes Verhalten
- Die GUI-Konsole soll exakt die vollständige Python-Logausgabe (wie im Terminal) anzeigen, inklusive aller Startup- und Systemmeldungen.

## Analyse
- Die GUI erhält offenbar nur einen gefilterten Log-Stream (UI-Traces), nicht aber den vollständigen Logbuffer.
- Die Backend-API (z. B. `get_konsole`, `get_logbuffer`) liefert vermutlich nicht alle Log-Einträge oder der Buffer wird zu früh geleert/zu stark gefiltert.
- Im Frontend (`app.html`) wird beim Öffnen des Debug-Tabs nicht der komplette Logbuffer geladen, sondern nur neue Einträge oder UI-Traces.

## Lösungsvorschlag
- Sicherstellen, dass der Logbuffer im Backend alle Log-Einträge (inkl. Startup, Environment, Session, DB, Browser etc.) enthält und über die API bereitstellt.
- Das Frontend muss beim Tab-Wechsel den vollständigen Logbuffer abfragen und anzeigen.
- Keine Filterung oder vorzeitige Löschung der relevanten Log-Messages.

## Nächste Schritte
- Backend: Logbuffer-Implementierung und API prüfen/erweitern.
- Frontend: API-Aufruf und Rendering anpassen, sodass die vollständigen Logs angezeigt werden.

**Ergebnis:**
- Erst nach diesen Anpassungen spiegelt die GUI-Konsole exakt die Backend-Konsole wider.
