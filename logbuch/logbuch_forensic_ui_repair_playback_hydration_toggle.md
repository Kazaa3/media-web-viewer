# Logbuch: Forensic UI Repair – Playback Crash & Hydration Toggle Stabilization

## Problemstellung
- **Playback Crash:** Ein harter JavaScript-Fehler (TypeError: Assignment to constant variable) verhindert die Wiedergabe, da `currentPlaylist` als const in audioplayer.js deklariert und im orchestrator (app_core.js) neu initialisiert wird.
- **Mock Toggle:** Die M/R/B-Buttons aktualisieren zwar die LEDs, lösen aber keinen Daten-Refresh aus – die Ansicht bleibt veraltet.

## Maßnahmen
### 1. Orchestrator-Layer (JS)
- [MODIFY] app_core.js
    - `window.currentPlaylist = []` als globale let-Variable deklariert.
    - `addToQueue` nutzt die globale Referenz und loggt die Operation.
- [MODIFY] audioplayer.js
    - Die alte const-Declaration von `currentPlaylist` entfernt, um Namenskollisionen und Zuweisungsfehler zu verhindern.

### 2. Hydration & Navigation (JS)
- [MODIFY] common_helpers.js
    - `setHydrationMode` ruft nach Backend-Bestätigung direkt `loadLibrary()` auf.
    - Forensisches Logging für den State-Übergang ergänzt.

### 3. Backend-Logistik (Python)
- [MODIFY] main.py
    - `set_hydration_mode` um [HYDR-TRACE]-Logs erweitert, um die Synchronisation zu dokumentieren.

## Verifikation
- [Automatisiert] Browser-Konsole auf TypeError: Assignment to constant variable nach Play-Klick prüfen.
- [Automatisiert] app.log auf [HYDR-TRACE] Hydration mode updated to: both prüfen.
- [Manuell] 'M' (Mock)-Button klicken und prüfen, ob die Bibliothek sofort aktualisiert wird.
- [Manuell] Play auf ein Item klicken und prüfen, ob es ohne Crash zur Queue hinzugefügt und abgespielt wird.

---

*Letztes Update: 18.04.2026*
