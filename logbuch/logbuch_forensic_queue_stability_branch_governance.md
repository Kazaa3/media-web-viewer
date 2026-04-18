# Logbuch: Forensic Queue Stability & Branch Governance

## Problemstellung
- Im "Alle Medien"-Modus wurde nur ein Medientyp (z.B. Fotos) angezeigt, da sich die Renderer gegenseitig überschrieben haben (Race Condition).
- Es besteht die Anforderung, die Queue-Filterung über zentrale Config-Flags branch-spezifisch zu steuern.

## Maßnahmen
### Konfiguration
- [MODIFY] config_master.py
    - Neue Flags hinzugefügt:
        - `force_queue_audio_branch`: Zeigt nur Audio-Items in der Queue.
        - `force_queue_multimedia_branch`: Zeigt nur Video/Multimedia.
        - `force_queue_extended_branch`: Zeigt alle erweiterten Forensik-Objekte.
    - Flags in der `ui_flag_registry` registriert, damit sie im Technical HUD steuerbar sind.

### Logik (Frontend)
- [MODIFY] playlists.js
    - Funktion `clearQueueContainers()` implementiert: Leert alle relevanten Queue-Container zentral.
    - `syncQueueWithLibrary()` ruft `clearQueueContainers()` am Anfang des Refresh-Pulses auf.
    - Branch-Filterlogik implementiert: Die neuen Flags bestimmen, welche Items in die Renderer gelangen.
- [MODIFY] audioplayer.js
    - `list.innerHTML = '';` aus `renderAudioQueue()` und `renderPhotoQueue()` entfernt, wenn `window.activeQueueFilter === 'all'`.
    - Renderer fügen nur noch Items hinzu, Container wird zentral geleert.
- [MODIFY] video.js
    - `list.innerHTML = '';` aus `renderVideoQueue()` entfernt, wenn unified view aktiv ist.

## Verifikation
- Im Modus "Alle Medien" werden jetzt Audio, Video und Fotos gemeinsam angezeigt.
- Das Setzen der Branch-Flags im Config zeigt gezielt nur die gewünschten Medientypen an.

---

*Letztes Update: 18.04.2026*
