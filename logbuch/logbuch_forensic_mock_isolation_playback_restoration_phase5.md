# Logbuch: Forensic Mock Isolation & Playback Restoration (Phase 5)

## Problemstellung
- "Realistic Mocks" erscheinen im Produktivmodus und verfälschen die Datenbasis.
- Audio-Playback ist defekt, da das Frontend noch die alte /media/-Route nutzt, während das Backend /stream/via/direct/ erwartet.
- Mocks werden zu früh im Hydrationszyklus injiziert.

## Maßnahmen
### 1. Backend: Mock Stage 5 & Striktes Filtering (Python)
- [MODIFY] main.py
    - "Realistic Mocks" werden nur noch in Stage 5 (audit_stage == 5) generiert und injiziert.
    - Vor Rückgabe von final_media im Real-Modus erfolgt ein strikter is_mock-Cleanup.
    - [PLAY-TRACE]-Logs an den Streaming-Endpunkten und in play_media hinzugefügt.

### 2. Frontend: Playback-Route-Angleichung (JS)
- [MODIFY] audioplayer.js
    - playAudio verwendet jetzt /stream/via/direct/ statt /media/ als proxyUrl.
    - [FE-PLAY]-Logs erfassen die exakte URL, die an das HTML5-Audioelement übergeben wird.

### 3. Forensic Trace Expansion (JS/Python)
- [MODIFY] config_master.py
    - audit_registry um Stage-5-Mock-Injektion erweitert.

## Verifikation
- [Automatisiert] app.log auf [MOCK-TRACE] Stage 5 reached. Injecting ... prüfen.
- [Automatisiert] app.log auf [PLAY-TRACE] Requesting direct stream for: <path> prüfen.
- [Manuell] Audio-Playback funktioniert wieder beim Klick auf ein Item in der Queue.
- [Manuell] Umschalten zwischen "Real" und "Both" zeigt Mocks nur noch, wenn Stage 5 aktiv ist.

---

*Letztes Update: 18.04.2026*
