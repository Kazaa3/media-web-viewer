# Implementation Plan: Playback Stabilization & mpv_wasm Integration (v1.46.046-REV2)

## Context
Dieses Update stellt die Systemstabilität wieder her, behebt den Datenbank-Boot-Loop und synchronisiert die Media-Pipelines mit dem neuen /stream/via/direct/-Standard.

---

## User Review Required

### DB Locking
- In `db.py` wurde bereits ein Threading-Lock (`_DB_INIT_LOCK`, `_INIT_IN_PROGRESS`) implementiert, um init_db-Loops zu verhindern. Kritischer Stabilitätsfix.

### Naming Consistency
- Die WASM-Engine bleibt als `mpv_wasm` benannt. Kein Umbenennen zu `vsm`.

### Streaming Alignment
- Audio- und Video-Direct-Modi nutzen nun beide das einheitliche `/stream/via/direct/`-Endpoint für forensisches Auditing.

---

## Proposed Changes

### [Backend]
#### [MODIFY] `db.py` [DONE]
- `_DB_INIT_LOCK` und `_INIT_IN_PROGRESS` implementiert.
- `init_db` optimiert: Gibt sofort zurück, wenn bereits initialisiert.

#### [MODIFY] `audio_handler.py` [DONE]
- Direct Stream URL auf `/stream/via/direct/` aktualisiert.

#### [MODIFY] `video_handler.py`
- Konsistentes Payload-Format für `mpv_wasm` und `direct`-Modi sicherstellen.

### [Frontend]
#### [MODIFY] `video.js`
- Prüfen, dass der `mpv_wasm`-Modus korrekt `window.mpvPlayer` triggert.
- Chrome-Engine-Auswahl für `direct`/`mse`/`hls`-Modi härten.

---

## Verification Plan

### Automated Tests
- `media_viewer.log` auf verbleibende `[BD-AUDIT]`-Rekursion überwachen.
- Prüfen, dass `[PLAY-PULSE]`-Logs sowohl Audio- als auch Video-Routing erfassen.

### Manual Verification
- MP3 (Audio Pipeline) und MP4 (Video Pipeline) abspielen.
- WebM-Datei testen, um sicherzustellen, dass der `mpv_wasm`-Engine getriggert wird.

---

(See <attachments> above for file contents. You may not need to search or read the file again.)
