# Logbuch: Media Viewer v1.35.68 Upgrade & Centralized Diagnostic Hub

## Zusammenfassung
Dieses Logbuch dokumentiert die wichtigsten Änderungen und die Stabilisierung des Media Viewers auf Version 1.35.68 mit Fokus auf die neue Centralized Diagnostic Hub-Funktionalität.

### 1. Versioning Synchronization
- **VERSION:** Aktualisiert von 1.34 auf 1.35.68.
- **src/core/main.py:** Interne VERSION-Konstante und Docstrings aktualisiert.
- **web/js/environment.js:** Frontend-Version auf 1.35.68 synchronisiert.

### 2. Centralized Diagnostic Hub
- **Debug-Tab (Options Panel):**
  - Direct Scan: Ein-Klick-Trigger zum Löschen und Re-Indexieren der SQLite-Datenbank aus ./media.
  - Atomic Sync: Speicherbasierte Synchronisation für sofortiges UI-Update.
  - Log Level Control: Echtzeit-Steuerung der Backend-Log-Verbosity (DEBUG, INFO, WARNING, ERROR).

### 3. Atomic Hydration Watcher
- **audioplayer.js:**
  - Automatischer Service, der alle 30s die Player-Queue hydriert und "Zombie"-Items entfernt.
  - Stellt sicher, dass die Queue nie leer bleibt und die UI synchron bleibt.

### 4. Backend Diagnostic APIs
- **main.py:**
  - `@eel.expose def set_log_level(level)`: Dynamische Anpassung des Python-Loglevels.
  - `@eel.expose def run_direct_scan()`: Vollständiger Medien-Scan und Re-Index.
  - `@eel.expose def sync_library_atomic()`: Sofortige Synchronisation der Datenbank mit der UI.

### 5. Verifikation
- **Version Sync:** 1.35.68 wird in allen Schichten korrekt angezeigt.
- **Diagnostic Hub:** Direct Scan und Atomic Sync funktionieren und kommunizieren mit dem Backend.
- **Watcher:** 30s-Heartbeat hält die Queue konsistent und entfernt fehlerhafte Items.

## Tipp
Nutze den Direct Scan-Button im Options-Panel, wenn Medien fehlen oder sich ./media stark verändert hat.

## Status
- **Stabilisiert:** System ist bereit für produktiven Einsatz und weitere Erweiterungen.
- **Dokumentation:** Siehe walkthrough_v13568_upgrade.md für Details und Screenshots.
