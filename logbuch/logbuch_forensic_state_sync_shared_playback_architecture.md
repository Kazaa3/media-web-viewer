# Logbuch: Forensic State Synchronization – Shared Playback Architecture

## Problemstellung
- Der "Shared Playback State" (Queue, Index, Current Item) soll im Backend gespiegelt und über globale Flags in config_master.py steuerbar sein.
- Ziel: Die Workstation-State ist forensisch auditierbar und bleibt über Pulses hinweg persistent.

## Maßnahmen
### 1. Konfigurationslogistik (Python)
- [MODIFY] config_master.py
    - Einführung von `SHARED_PLAYBACK_STATE = {"queue_count": 0, "active_index": -1, "active_path": None}`.
    - Hilfsfunktion zum sicheren Aktualisieren dieser Flags.

### 2. Backend-Orchestrierung (Python)
- [MODIFY] main.py
    - Implementierung von `@eel.sync_playback_state(payload)`: Aktualisiert `config_master.SHARED_PLAYBACK_STATE` und erzeugt einen [STATE-TRACE]-Logeintrag für jede Änderung.

### 3. Frontend-Orchestrierung (JS)
- [MODIFY] app_core.js
    - `addToQueue` ruft nach lokalen Updates `eel.sync_playback_state()` auf.
    - `play` (Orchestrator) broadcastet den "Active Item"-State an das Backend.

## Verifikation
- [Automatisiert] Nach addToQueue im UI erscheint im app.log: [STATE-TRACE] Playback Context Updated: Items=1, Active=/path/to/media.mp3
- [Manuell] Mehrere Items zur Queue hinzufügen und prüfen, ob der backend-Log den wachsenden queue_count korrekt abbildet.
- [Manuell] Track wechseln und prüfen, ob active_path im Log aktualisiert wird.

---

*Letztes Update: 18.04.2026*
