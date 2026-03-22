# Logbuch: App-GUI Neustart & Reset

## Hintergrund

In komplexen Medien-Apps wie Media Web Viewer ist eine zuverlässige Neustart- und Reset-Funktion für die GUI essenziell. Sie ermöglicht das Wiederherstellen eines konsistenten Zustands, behebt UI-Fehler und sorgt für stabile Sessions.

## Warum nötig?
- **Session-Probleme:** Nutzer können inkonsistente States erleben (z. B. nach Netzwerkfehlern oder Backend-Neustarts).
- **UI-Fehler:** Frontend kann hängen oder nicht korrekt reagieren (z. B. nach Tab-Switch-Loop oder WebSocket-Fehler).
- **Cache/State:** Hard-Reset setzt alle Caches und Sessions zurück, Soft-Reset nur das Frontend.

## Funktionstypen
- **Soft-Reset:** Frontend reload (`window.location.reload()`), behebt UI-Probleme ohne Backend-Neustart.
- **Hard-Reset:** Backend-Prozess wird neu gestartet (z. B. per API-Call, Docker-Restart), setzt alle Sessions zurück.

## Implementierung
- UI-Button für Neustart/Reset (Soft/Hard).
- Backend-API für Hard-Reset (z. B. `os.execv`, Supervisor, Docker).

## Vorteile
- Stabile App, weniger Fehler durch inkonsistente States.
- Nutzer können selbst Fehler beheben.

## Hinweise
- Nach Hard-Reset: Nutzer müssen sich neu verbinden.
- Für Docker: `docker restart <container>`.

---
