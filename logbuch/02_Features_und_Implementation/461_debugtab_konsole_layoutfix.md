# Debug-Tab & Konsolen-Layout: Änderungen & Fixes

**Datum:** 14.03.2026

## 1. Bereinigung der Konsole (rechte Spalte)
- **Problem:** Die Konsole wurde mit vollständigen JSON-Daten der gesamten Mediathek überflutet, da in den Funktionen `scan_media` und `loadLibrary` bei jedem Update die komplette Datenbankliste stumpf in das Konsolenfeld (`debug-output`) geschrieben wurde.
- **Lösung:** Diese Zuweisungen wurden entfernt.
- **Ergebnis:** Die Konsole zeigt jetzt ausschließlich echte Python-Logs und UI-Traces (z. B. `[Scan-Trace]`, `switchTab`) an.

## 2. Neupositionierung der Laufzeit-Info
- Das Element **"Laufzeit-Info & Log-Level"** wurde von der linken in die rechte Spalte verschoben (direkt über die Konsole).
- Das Design wurde an das dunkle Theme der rechten Spalte angepasst (dunkler Hintergrund, helle Schrift für PIDs), sodass es sich nahtlos in den Konsolenbereich einfügt.

## 3. Log-Level Persistenz
- Das Log-Level-Menü erkennt jetzt, wenn eine manuelle Auswahl getroffen wurde, und überschreibt diese nicht mehr sofort durch automatische Hintergrund-Updates (mittels `dataset-Flag manual`).

---

### Neues Layout im Debug- & DB-Tab

- **Links:** Item-DB (Übersicht/Statistiken)
- **Mitte:** Python-Dict (Details) – Hier erscheint weiterhin das formatierte JSON der Datenbank/Items für Detail-Inspektionen.
- **Rechts oben:** Laufzeit-Info (PIDs & Log-Level-Wahl)
- **Rechts unten:** Konsole (nur echte Logs, sauber gefiltert)

---

**Ergebnis:**  
Die Konsole ist jetzt übersichtlich, zeigt nur relevante Logs und UI-Traces, und die Laufzeit-Info ist klar und thematisch passend platziert. Das Log-Level bleibt bei manueller Auswahl stabil.
