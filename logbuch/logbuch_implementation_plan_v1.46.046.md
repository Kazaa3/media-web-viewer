# Implementation Plan: Playback Stabilization & VSM Integration (v1.46.046)

## Context
Dieses Update behebt das "playback goes not"-Problem, den init_db Boot-Loop und integriert den 'vsm' (WASM) Modus formal. Zudem werden Audio- und Video-Pipelines strikter getrennt.

---

## User Review Required

### DB Recovery Pulse
- In `db.py` wird ein strikter Semaphore-Guard zu `init_db` hinzugefügt.
- Verhindert Boot-Loop-Spam, indem nur ein Initialisierungszyklus pro PID erlaubt ist.

### VSM Mode Integration
- Der Modus `mpv_wasm` wird im gesamten Orchestrator und Frontend in `vsm` umbenannt/aliased.
- Entspricht den forensischen Standards und sorgt für Konsistenz.

---

## Proposed Changes

### [Backend]
#### [MODIFY] `db.py`
- **Hardened init_db:**
    - Implementiere `_DB_INIT_LOCK` (boolean), um gleichzeitige/rekursive Aufrufe zu verhindern.
    - Setze `_DB_INITIALIZED` so früh wie möglich.
    - Verbessere Error-Logging für leere Exceptions im Migrationsblock.

#### [MODIFY] `mode_router.py`
- **vsm Identification:**
    - `smart_route` gibt jetzt `vsm` statt `mpv_wasm` zurück.
    - Aktualisiere die Mode-Beschreibungs-Mappings.

#### [MODIFY] `video_handler.py`
- **Payload Alignment:**
    - `process()` bridged den `vsm`-Modus korrekt zum Frontend-Handshake.

### [Frontend]
#### [MODIFY] `video.js`
- **vsm Support:**
    - Orchestrator prüft auf `source.mode === 'vsm'`.
    - Mappt `vsm` auf das `window.mpvPlayer` Canvas-Engine.

---

## Open Questions
- Soll der `mpv_wasm`-Binary-Ordner auch in `vsm` umbenannt werden? (Vorschlag: Vorerst nicht, nur Alias im Code).

---

## Verification Plan

### Automated Tests
- PLAY-PULSE-Logs während Playback erfassen, um die vsm-Entscheidungslogik zu prüfen.
- Sicherstellen, dass `init_db` nur einmal pro Session startet/loggt.

### Manual Verification
- MP3 abspielen und prüfen, dass es die smart_route-Video-Logik umgeht ("Own Pipe"-Separation).
- WebM-Datei abspielen und prüfen, dass der vsm-Engine im UI getriggert wird.

---

(See <attachments> above for file contents. You may not need to search or read the file again.)
