# Media Viewer v1.35.68 Stabilization & Diagnostic Hub

## Ziel
Upgrade auf v1.35.68, Einführung eines zentralen Diagnostic Hubs und Sicherstellung der Systemstabilität.

## Umsetzungsschritte

### 1. Environment & Utilities
- **[RUN] super_kill.py:**
  - Alle Zombie-Prozesse beenden und Port 8345 freigeben.

### 2. Version Synchronization (v1.35.68)
- **[MODIFY] VERSION:**
  - Inhalt auf 1.35.68 aktualisieren.
- **[MODIFY] main.py:**
  - VERSION-Konstante und Doku-Strings aktualisieren.
- **[MODIFY] JS Files:**
  - Version-Strings in environment.js, audioplayer.js und weiteren relevanten Dateien aktualisieren.

### 3. Backend Enhancements
- **[MODIFY] main.py:**
  - `@eel.expose def set_log_level(level)` implementieren, um Log-Level in Echtzeit aus der UI zu steuern.
  - Logger-State dynamisch aktualisieren.

### 4. Frontend Enhancements
- **[MODIFY] options_panel.html:**
  - "Centralized Diagnostic Hub"-Sektion integrieren.
  - Echtzeit-Loglevel-Buttons und DOM Health Auditor-Controls hinzufügen.
- **[MODIFY] audioplayer.js:**
  - [NEW] `startAtomicHydrationWatcher()` implementieren, um die Queue zu überwachen und bei Inkonsistenz automatisch zu hydrieren.

### 5. Library Sync
- **[EXECUTE] DB Hydration & Direct Scan:**
  - Indexing-Scanner ausführen, um die Bibliothek mit echten Medien aus ./media zu befüllen.

## Offene Fragen
- Soll `startAtomicHydrationWatcher` automatisch beim Start laufen oder nur im Diagnostic Mode?
- Soll der "Direct Scan" via main.py (Eel) oder als separater CLI-Befehl getriggert werden?

## Verifikation
### Automatisierte Tests
- `scripts/verify_playback.py` ausführen, um Kernfunktionalität zu prüfen.
- Backend-Logs auf `[System] Version Parity: 1.35.68` prüfen.

### Manuelle Verifikation
- Prüfen, ob der "Diagnostic Hub" im Options-Panel sichtbar ist.
- Log-Level in der UI ändern und Backend-Output auf veränderte Verbosity prüfen.
- Sicherstellen, dass die Audio-Player-Queue nach einem Scan korrekt hydriert wird.

## Status
- **Bereit:** Plan dokumentiert, offene Fragen zur Ausführung geklärt.
- **Warten auf:** User-Feedback zu Watcher- und Scan-Trigger-Strategie.
