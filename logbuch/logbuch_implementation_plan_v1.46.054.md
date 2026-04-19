# Plan: Forcing Real Media Ingestion & Scanner Visibility

## Kontext
Der Screenshot des Nutzers zeigt, dass zwar die Mock-Metadaten repariert sind, aber das "Scanner Dashboard" nicht zuverlässig die 12-Item-Mock-Ansicht übersteuert. Ein erneuter Scan ist nötig, um echte Medien einzulesen.

---

## User Review Required

### Wichtige Maßnahmen
- `rescan_on_boot: True` wird im Master-Config gesetzt, damit beim nächsten Start automatisch das media/-Verzeichnis indiziert wird.

---

## Proposed Changes

### Forensic Visibility Hardening
#### [MODIFY] `bibliothek.js`
- Die Prüfung `realDbCount === 0` wird ganz an den Anfang von `renderLibrary` verschoben.
- Bei 0 echten Assets wird sofort das Scanner Dashboard angezeigt (Early Return), sodass Mocks nicht mehr den Scan-Bedarf "verstecken" können.
- Granulares Console-Logging ([FE-AUDIT]) ergänzt, um zu verfolgen, warum das Dashboard erscheint oder nicht.

### Configuration Preset
#### [MODIFY] `config_master.py`
- Default für `rescan_on_boot` von `False` auf `True` ändern (mindestens für diese Session), damit der gewünschte Boot-Scan ausgeführt wird.

### Library Handshake
#### [MODIFY] `main.py`
- Sicherstellen, dass der Hintergrund-Boot-Scan das Frontend nach Abschluss korrekt signalisiert, sodass das Dashboard automatisch verschwindet, sobald echte Items gefunden werden.

---

## Verification Plan

### Automated Tests
- Keine (User wünscht "ohne playwright und selenium").

### Manual Verification
- Über die Konsole prüfen, dass der Boot-Scan gestartet wurde (Log-Ausgabe).
- Sicherstellen, dass das Forensic Scanner Dashboard auch bei aktivierten Mocks sichtbar ist, wenn DB: 0.

---

(See <attachments> above for file contents. You may not need to search or read the file again.)
