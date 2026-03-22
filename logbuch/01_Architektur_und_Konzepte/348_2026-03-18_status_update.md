# Logbuch - 18. März 2026

## Status Update: Erfassen von Parser-Performance & UI-Optimierung

### Erreichte Meilensteine

1.  **Reporting Dashboard Erweiterung**:
    *   Die `get_parser_stats` Funktion im Backend liefert nun detaillierte Metriken.
    *   Anzeige der durchschnittlichen Parser-Zeiten im Reporting-Tab.
    *   Neuer Bereich: **Latest Parser Results** – Eine Tabelle der letzten 20 gescannten Dateien mit Einzelzeiten pro Parser.
    *   Fix: `eel.get_parser_stats` war zeitweise nicht erreichbar, da die Funktionsdefinition nach dem blockierenden `eel.start` Aufruf lag. Code wurde modularisiert und nach oben verschoben.

2.  **Optionen Tab Restrukturierung**:
    *   Umstellung auf ein **Sub-Tab System** innerhalb der Optionen:
        *   **Allgemein**: Scan-Verzeichnisse, App-Modus, Debug-Flags.
        *   **Tools**: HandBrake Integration, WebM Konvertierung, VLC Stream & Playlist Tools.
        *   **System**: Detaillierte Environment-Info, Kernarchitektur, Paket-Status.
    *   Verbesserte Usability durch vertikales Scrolling in den Sub-Bereichen.

3.  **UI & Layout Fixes**:
    *   Behebung eines kritischen Nesting-Fehlers bei den `div`-Containern im Optionen-Tab. Dies verhinderte, dass nachfolgende Tabs (Parser, Tests, Debug) korrekt gerendert wurden.
    *   Synchronisierung der Scroll-Logik über alle neuen Ansichten.

### Offene Punkte & Next Steps

*   [ ] **M4P Video Support**: Untersuchung der schwarzen Anzeige bei Audio-Wiedergabe.
*   [ ] **WebRTC / WHEP Integration**: Implementierung für Echtzeit-Streaming.
*   [ ] **Parser-Detail-Einstellungen**: Funktionalität für das neue "Parser-Optionen" Panel hinzufügen.
*   [ ] **HandBrake Progress**: Parsen von `stderr` für Fortschrittsanzeige bei Transcodierung implementieren.

### Fazit
Das System ist nun deutlich übersichtlicher und bietet tiefe Einblicke in die Performance der Metadaten-Extraktion. Die Architektur ist bereit für die nächsten Erweiterungen im Video-Streaming Bereich.
