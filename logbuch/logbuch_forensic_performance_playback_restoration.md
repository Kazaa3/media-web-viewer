# Logbuch: Forensic Performance & Playback Restoration

## Problemstellung
- **Bootstrap Block:** Stale mwv.lock-Datei verhindert Start nach Crash.
- **UI Event Bloat:** Mehrfachklicks auf Hydration-Buttons führen zu Lag und Thread-Lock.
- **Silent Playback Failure:** Audio-Fehler werden nicht forensisch geloggt.
- **Rendering Black Hole:** 516 Items werden gezählt, aber nicht angezeigt, da list.appendChild(fragment) im Renderer fehlt.

## Maßnahmen
### 1. Backend Bootstrap (Python)
- [MODIFY] main.py
    - In `start_app()`: Wenn acquire_lock() fehlschlägt, prüfe, ob der PID im Lockfile noch läuft. Falls nicht, führe auto-cleanup aus und starte neu.

### 2. UI Performance Guard (JS)
- [MODIFY] common_helpers.js
    - window.__mwv_ui_locked-Debounce in setHydrationMode implementiert (1,5s Cooldown).
    - Visuelles Feedback (Opacity/Spinner) während "Syncing".

### 3. Forensic Playback Diagnostic (JS)
- [MODIFY] audioplayer.js
    - initAudioPipeline(): onwaiting, onstalled, onerror Listener am Audioelement.
    - MediaError-Codes (1-4) werden forensisch geloggt ([PLAYBACK-DIAG]).

### 4. Queue Rendering (JS)
- [MODIFY] audioplayer.js
    - In renderAudioQueue():
        - list.innerHTML = ''; vor der Injektion wiederhergestellt.
        - list.appendChild(fragment); nach dem Item-Loop wiederhergestellt.
        - [RENDER-STEP]-Logs für Target Selection, Filtration, DOM Creation, Final Injection.
    - isVideoItem() strikter: Nur echte Videos werden als Video erkannt.

### 5. Forensic Trace (JS)
- [MODIFY] bibliothek.js
    - [HB-TRACE] (Handshake-Broadcast) loggt den Datenfluss von Speicher bis Renderer.

## Verifikation
- [Automatisiert] Dummy-mwv.lock erzeugen, App startet trotzdem (Auto-Cleanup).
- [Automatisiert] Konsole zeigt [PLAYBACK-DIAG] und [RENDER-STEP] für alle Items.
- [Manuell] M/R/B-Buttons mehrfach klicken: GUI bleibt responsiv.
- [Manuell] REFRESH: Liste zeigt 516 Items, kein "Black Void" mehr.

---

*Letztes Update: 18.04.2026*
