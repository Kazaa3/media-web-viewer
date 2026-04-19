# Forensic Workstation: Separated Player Architecture (v1.45.150)

## Zielsetzung
Die Audio- und Video-Player-Architekturen werden vollständig entkoppelt. Die neue "Forensic Workstation" (Rebuild Mode) setzt auf ein professionelles 3-Spalten-Layout:

- **Linke Sidebar:** Kontext-Navigation, Filter, Metadaten
- **Center Stage:** Aktiver Player (Audio oder Video, je nach Item)
- **Rechte Inventory:** Item-Liste und Queue

## Änderungen & Komponenten

**[Component] UI: PLAYER MODULE SEPARATION**
- **audioplayer.html:** Neuer, eigenständiger Audio-Player-Fragment mit Waveform-Visualisierung und präzisen Controls.
- **video_player.html:** Cleanup, keine Audio-Logik mehr enthalten.

**[Component] UI: REBUILD WORKSTATION LAYOUT**
- **forensic_workstation.html:** Hauptcontainer für das neue Workstation-View, implementiert das 3-Spalten-Layout (CSS Grid/Flex).
- **shell_master.html:** Lädt forensic_workstation.html automatisch im REBUILD-Mode.

**[Component] LOGIC: ORCHESTRATION BRIDGE**
- **app_core.js:** Neue Funktion `injectPlayerIntoStage(item)`, die je nach Item-Typ dynamisch den passenden Player-Fragment in die Center Stage lädt.

## Entscheidungsnotiz
- Die rechte Item-Liste ist als feste Sidebar (z.B. 350px) vorgesehen, kann aber per Hotkey ein-/ausgeblendet werden.

## Verifikationsplan
- **Automatisierte Tests:**
    - Fragment Loader Test: Wechsel von MP3 zu MP4 tauscht die Player-Fragmente im Forensic Stage ohne Reload.
- **Manuelle Prüfung:**
    - 3-Spalten-Layout auf Resizing testen.
    - Sidebar bleibt persistent, Player werden in der Center Stage dynamisch getauscht.

**Status:**
- Architektur ist vorbereitet für weitere Spezialisierungen und garantiert eine saubere Trennung der Player-Logik.
