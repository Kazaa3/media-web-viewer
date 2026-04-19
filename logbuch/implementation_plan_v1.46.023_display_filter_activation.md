# Implementation Plan: Display Filter Activation & Forensic Refinement (v1.46.023)

## Ziel
Die "Mediengalerie"-Filterfunktion (ALLE MEDIEN Dropdown) wird aktiviert und mit der zentralen Synchronisationspipeline verbunden. Dadurch kann die Medienanzeige nach Kategorie (Audio, Video, etc.) gefiltert werden.

## Schritte

### 1. Global Orchestrator (web/js/app_core.js)
- **Event Listener:**
  - Funktion `hydrateCategoryDropdown` aktualisieren, sodass automatisch ein `change`-Event-Listener an `#queue-type-filter` angehängt wird.
- **Hydration Pulse:**
  - Listener aktualisiert `window.activeQueueFilter` und triggert `syncQueueWithLibrary()`.

### 2. Unified Playlist Engine (web/js/playlists.js)
- **Global Filter State:**
  - `window.activeQueueFilter = 'all'` explizit initialisieren, um undefined-Fehler beim ersten Hydrationslauf zu vermeiden.
- **Category Filtering:**
  - `syncQueueWithLibrary()` so erweitern, dass Items nach `window.activeQueueFilter` gefiltert werden (Vergleich von Kategorie/Typ mit Dropdown-Auswahl).
- **Render Pulse:**
  - Nach Filterwechsel sofort `renderAudioQueue()` und `renderVideoQueue()` aufrufen, damit UI und "Titel"-Zähler in Echtzeit aktualisiert werden.

## Verifikationsplan

### Automatisierte Tests
- Anwendung starten: `python3 src/core/main.py --probe`
- Im Probe-Modus Filterwechsel simulieren (z.B. `queue-type-filter` auf "video" setzen) und prüfen, dass nur Video-Items in `currentPlaylist` verbleiben.

### Manuelle Überprüfung
- "audio" im Dropdown wählen: `.pdf` und `.jpg` verschwinden aus der Liste.
- "ALLE MEDIEN" wählen: Alle Items erscheinen wieder.
- "Titel"-Zähler (z.B. "501 Titel") aktualisiert sich dynamisch entsprechend der Filterauswahl.

## Status
- Die Filterfunktion wird von einem "Zombie"-UI-Element zu einer voll funktionsfähigen Komponente aufgewertet.
- Die Änderungen sorgen für eine forensisch präzise Medienauswahl und eine bessere Nutzererfahrung.

---

**Freigabe erforderlich:**
Bitte bestätigen Sie, ob diese Änderungen wie beschrieben umgesetzt werden sollen.