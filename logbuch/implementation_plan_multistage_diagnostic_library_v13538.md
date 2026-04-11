# 🗺️ Implementation Plan — Multi-Stage Diagnostic Library (v1.35.38)

## Ziel
Sowohl System-Mocks (für Fehlerfall-Tests) als auch echte Assets (für Recovery- und Playback-Tests) werden gleichzeitig im Player sichtbar und testbar gemacht. Die Diagnostik-Suite wird um eine Multi-Stage-Hydration erweitert.

---

## Key Goals

- **Multi-Stage Hydration:**
  - Die Funktion `Diagnostics.hydrate()` in `mwv_diagnostics.js` wird so erweitert, dass sie 4 Test-Tracks injiziert:
    - **Stage 1 & 2 (Negative Test):**
      - Zwei Items mit absichtlich ungültigen/falschen Pfaden (`sample_audio.mp3`), um Playback-Fehler und Fallback-UI zu testen.
    - **Stage 3 & 4 (Positive Test):**
      - Zwei Items mit echten, im Workspace vorhandenen Dateien (`Einfach & Leicht.mp3`, `Viva La Vida.opus`), um die vollständige Playback-Kette zu verifizieren.
  - Jeder Track wird im Titel mit seiner Stage gekennzeichnet (z.B. `[STAGE 1] Missing File Test`).

- **Ultra-Robuste Datenstruktur:**
  - Alle Items werden nach dem neuen Modell (models.py) gebaut, sodass nie „Unknown Title“ angezeigt wird.

- **Datenintegrität:**
  - Die Queue zeigt nach Boot exakt 4 Titel.

---

## Umsetzungsschritte

1. **mwv_diagnostics.js**
   - Funktion `hydrate()` so erweitern, dass sie die vier Test-Tracks mit allen erforderlichen Feldern (id, name, artist, album, path, category, is_mock, tags) injiziert.
   - Negative Stages: Pfad auf nicht existierende Datei setzen, Titel und Artist explizit setzen.
   - Positive Stages: Pfad auf echte Datei im media/-Ordner setzen, Titel und Artist explizit setzen.
   - Items in `allLibraryItems` und `currentPlaylist` pushen, falls noch nicht vorhanden.
   - Nach Hydration: `renderPlaylist()` und `renderLibrary()` aufrufen.

2. **UI/UX**
   - Im Player-Tab erscheinen alle vier Titel, klar gekennzeichnet.
   - Fehlerhafte Tracks lösen einen Fehler-Toast aus, echte Tracks spielen ab.

3. **Verifikation**
   - Nach Boot: „4 Titel“ in der Queue.
   - Stage 1 & 2: Fehler-Toast und robuster Fallback-Text.
   - Stage 3 & 4: Sofortige Wiedergabe.

---

## Feedback
Soll diese Multi-Stage-Batterie wie beschrieben umgesetzt werden? Rückmeldung erwünscht!

---

**ArtifactType:** implementation_plan
**RequestFeedback:** true
**Summary:** Multi-Stage-Diagnostik für gleichzeitige Fehlerfall- und Recovery-Tests im Player.
