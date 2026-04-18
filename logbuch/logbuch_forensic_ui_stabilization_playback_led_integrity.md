# Logbuch: Forensic UI Stabilization – Playback & LED Integrity

## Problemstellung
- **Playback Crash:** ReferenceError: renderStart is not defined in audioplayer.js blockiert die Initialisierung des Audio-Players. Ursache: Die Performance-Benchmark-Variable wurde beim Refactor entfernt.
- **DB LED Pulse:** Die DB-LED bleibt gelb, weil der LED-Trigger vor Abschluss des Library-Handshakes (und damit vor dem Health-Status) feuert.

## Maßnahmen
### 1. Audio-Pipeline (JS)
- [MODIFY] audioplayer.js
    - In `renderAudioQueue` wird `const renderStart = performance.now();` am Einstiegspunkt definiert.
    - Performance-Logging am Ende des Render-Blocks ergänzt.

### 2. UI-Diagnostik (JS)
- [MODIFY] common_helpers.js
    - LED-Update-Logik in eine eigene Funktion `refreshForensicLeds()` ausgelagert.
    - Spezielle Behandlung für den 'ok'-Status, damit CSS-Farben korrekt angewendet werden.
- [MODIFY] bibliothek.js
    - Am Ende des `loadLibrary`-Handshakes wird `refreshForensicLeds()` aufgerufen, damit die DB-LED (Grün/Rot) den aktuellen Audit-Status widerspiegelt.

## Verifikation
- [Automatisiert] Browser-Konsole zeigt keinen ReferenceError mehr.
- [Automatisiert] Log: `[Queue-UI] renderAudioQueue completed in X ms` erscheint.
- [Manuell] Nach REFRESH wird die DB-LED grün (bei 'ok'-Status).
- [Manuell] Play auf ein Item: Audio startet, UI wechselt ohne Crash zum Player-Tab.

---

*Letztes Update: 18.04.2026*
