# Logbuch-Idee: Datenbank-Viewer als Zweit-Screen im dict

## Idee
Im dict-Frontend soll ein zweiter Screen/Tab integriert werden, der die aktuelle Datenbank (z.B. media_library.db) anzeigt und durchsuchen lässt.

## Konzept
- **Zweiter Screen/Tab:**
  - Im Web-Frontend (dict) ein zusätzlicher Tab oder Split-Screen für die Datenbankansicht.
  - Anzeige aller Medieneinträge, Filter- und Suchfunktion, ggf. Sortierung nach Spalten.
  - Optional: Details zu einzelnen Einträgen, Export/Download als CSV/JSON.
- **Technik:**
  - Backend-API liefert aktuelle DB-Inhalte (z.B. als JSON-Endpoint).
  - Frontend-UI (HTML/JS) rendert die Tabelle und bietet Interaktion.
  - Optional: Live-Refresh oder manuelles Reload.

## Umsetzungsideen
- Erweiterung von `main.py` um einen API-Endpunkt für den DB-Export.
- UI-Erweiterung in `web/app.html` für den neuen Tab/Screen.
- Optional: Admin-Features wie Löschen/Bearbeiten direkt aus der Ansicht.

## Status
Idee eingetragen – Bewertung, Design und Umsetzung offen.

## Stand
13. März 2026
