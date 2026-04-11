# Implementation Plan – Mock Data Bootstrap & UI Restoration

## Ziel
Die "Warteschlange leer"-Problematik wird durch ein robustes Mock-Daten-Bootstrap gelöst, sodass die Audio Player Queue immer befüllt ist – ideal für GUI-Validierung und Test.

---

## Proposed Changes

### [FRONTEND] Fail-Safe Queue Populator

**[MODIFY] audioplayer.js**
- **injectMockBootstrap():**
  - Wenn `currentPlaylist` beim Laden leer ist, wird eine fest kodierte Liste von v1.33-Sample-Tracks (z.B. "Anfangsstadium RMX", "Einfach & Leicht") injiziert.
  - `renderPlaylist()` wird direkt nach der Injektion aufgerufen.
- **syncQueueWithLibrary():**
  - Korrekte Filterung und Synchronisation von echten und Mock-Items.

**[MODIFY] bibliothek.js**
- Signalisiert `mwv_library_ready` auch bei Verwendung von Mock-Daten, damit der Audio Player synchronisieren kann.

---

### [BACKEND] Media Fetch Stability

**[MODIFY] main.py**
- **get_library:**
  - Gibt Mock-Items als JSON zurück, wenn die Medientabelle leer ist.
- **Konfiguration:**
  - `enable_mock_data = True` beim Start erzwingen.

---

## Verification Plan

### Automated Tests
- **Queue Audit:** Im Console-Log prüfen, dass `currentPlaylist.length > 0` beim Start.
- **Metadata Sync:** Mock-Track anklicken, Footer muss "Beginner" und "Hammerhart" anzeigen.

### Manual Verification
- **Screenshot Audit:** Rechte Queue ist nicht mehr leer.
- **Playback Trigger:** "Play"-Icon aktualisiert sich korrekt beim Mock-Track.

---

**User Review Required:**
- Sofortige Sichtbarkeit von Items in der Queue.
- Footer-Metadaten werden aus Mock-Daten korrekt übernommen.
- Nach GUI-Validierung folgt Troubleshooting des echten Media-Scans.
