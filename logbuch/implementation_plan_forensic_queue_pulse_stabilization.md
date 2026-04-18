# Implementation Plan: Forensic Queue Pulse Stabilization & Deep Logging

## Ziel
Die "Ghosting"-Probleme (Audio-Items verschwinden im Unified-View) und die Inkonsistenzen beim Hydration-Toggle werden nachhaltig behoben. Zusätzlich wird eine tiefe forensische Protokollierung eingeführt, um alle Rendering- und Filterstufen transparent nachvollziehen zu können.

---

## Maßnahmen

### 1. Structural Fixes & Atomic Clear
- [MODIFY] web/js/audioplayer.js
    - Rendering-Logik korrekt in `containers.forEach` verschachteln.
    - Redundantes `list.innerHTML = '';` entfernen.
    - DOM-Wipe-Check-Logs einbauen: Vor und nach jedem Renderer wird die Elementanzahl geloggt.
    - `mockFlag` korrekt im Loop definieren.
    - `renderPhotoQueue` und `renderVideoQueue` auf strukturelle Integrität prüfen.
- [MODIFY] web/js/video.js
    - Renderer so anpassen, dass kein redundantes Leeren mehr erfolgt.

### 2. Zentrale Orchestrierung & Branch-Governance
- [MODIFY] web/js/playlists.js
    - `clearQueueContainers()` implementieren.
    - `syncQueueWithLibrary()` orchestriert alle Renderer und loggt die Filtrationsstufen.
    - Branch-Filterlogik gemäß Config-Flags (force_queue_audio_branch, etc.).
- [MODIFY] src/core/config_master.py
    - Flags für Branch-Governance und alle Render-Pulse registrieren:
        - `force_queue_audio_branch`, `force_queue_multimedia_branch`, `force_queue_extended_branch`
        - `render_library_enabled`, `render_photo_queue_enabled`, `render_file_browser_enabled`, `render_audio_queue_enabled`, `render_video_queue_enabled`
    - Hydration-Mode auf "both" setzen.

### 3. UI/UX & Hydration Toggle
- [MODIFY] web/fragments/player_queue.html
    - REFRESH-Button ergänzen.
- [MODIFY] web/js/bibliothek.js
    - `refreshLibrary()`-Logik aktualisieren (Filter-Reset, Hydration-Mode setzen).
    - `renderLibrary()` mit Config-Flag absichern.
- [MODIFY] web/js/browse.js
    - `renderFileList()` mit Config-Flag absichern.
- [MODIFY] common_helpers.js
    - Medienerkennung (isVideoItem, isPhotoItem) auditieren.
    - Tiefe forensische Logging-Funktionen für setHydrationMode.
- [MODIFY] Hydration-LEDs
    - HUD und Footer LEDs synchronisieren.

---

## Verifikation
- "Alle Medien" zeigt gemischte Liste (Audio, Foto, PDF, Video) mit korrektem Count.
- Hydration-Toggle (Mock/Real/Both) ist synchronisiert und reagiert konsistent.
- Logs zeigen DOM-Element-Fortschritt, Filtrationsstufen und Kategorieverteilung.
- Branch-Flags im Config steuern die Queue wie erwartet.

---

*Letztes Update: 18.04.2026*
