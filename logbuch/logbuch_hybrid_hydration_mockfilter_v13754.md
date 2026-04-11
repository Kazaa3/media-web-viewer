# Logbuch v1.37.54 – Hybrid Library Hydration & Mock Filtering

**Datum:** 2026-04-06

## Ziel
Einführung eines "Hybrid"-Hydration-Systems: Gleichzeitige Anzeige echter Medien und diagnostischer Mock-Items, inkl. dediziertem UI-Filter zur gezielten Steuerung der Sichtbarkeit.

## Maßnahmen & Änderungen

### 1. Backend (Hybrid Connectivity)
- **main.py**
  - `get_library` liefert jetzt eine kombinierte Liste: alle echten DB-Items **plus** die 3 Stage-3-Diagnose-Mocks.
  - Mocks werden mit `is_mock: true` markiert, damit das Frontend sie unterscheiden kann.

### 2. Frontend (UI & Smart Filtering)
- **player_queue.html**
  - Dropdown: Neue Option "Diagnose (Mock-Items)" zum gezielten Anzeigen/Verstecken der Testdaten.
- **audioplayer.js**
  - Smart Primary Filter: `syncQueueWithLibrary` beachtet jetzt `window.activeQueueFilter`.
    - "Alle": Zeigt echte und Mock-Items (volle Transparenz).
    - "Diagnose": Zeigt nur die 3 Mocks.
    - Kategorie-Modi (Audio/Video): Blendet Mocks aus, sobald echte Items dieser Kategorie vorhanden sind.
  - Auto-Opening: Die Warteschlange (Queue) wird nach erfolgreicher Synchronisierung automatisch geöffnet.

## Offene Frage
- Sollen die Mocks im "Alle Medien"-Modus oben oder unten in der Liste erscheinen? (**Vorschlag:** Oben, für bessere Sichtbarkeit im Dev/Test.)

## Verifikation
- **Manuell:**
  - Boot: Player öffnet automatisch mit sichtbarer Queue.
  - Filter: "Alle Medien" zeigt 541 echte Items + 3 Mocks, "Diagnose" nur die 3 Mocks.
  - Video-Filter: "Video-Zweig" zeigt nur echte Filme, keine Mocks.

---
**Status:** Hybrid-Hydration & Mock-Filter-Logik dokumentiert (v1.37.54)
