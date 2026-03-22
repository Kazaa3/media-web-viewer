# Logbuch: Performance-Probleme – Chrome-native Videos werden unnötig in VLC Pipe gestartet (2026-03-15)

**Datum:** 2026-03-15

## Problem
- Videos wie MP4, die eigentlich Chrome-native abspielbar wären, werden im Modus "vlc pipe" trotzdem über FFmpeg→VLC gestartet.
- Dies führt zu unnötigen Performance-Einbußen (langsamer Start, höherer Ressourcenverbrauch), obwohl der Browser die Datei direkt und effizient abspielen könnte.

## Analyse
- Die aktuelle Logik startet im Modus "vlc pipe" immer den Pipe-Prozess, unabhängig davon, ob das Format browserkompatibel ist.
- Chrome-native Formate (z.B. MP4 mit H.264/AAC) sollten bevorzugt direkt im Browser abgespielt werden.
- Nur bei echten Inkompatibilitäten (MEDIA_ERR_SRC_NOT_SUPPORTED) ist der VLC Pipe sinnvoll.

## Empfehlungen
- Die Logik für "vlc pipe" so anpassen, dass zunächst ein nativer Chrome-Playback-Versuch erfolgt.
- Erst bei Fehler (Code 4) automatisch auf VLC Pipe umschalten (wie im Hybrid-Modus).
- Performance-Messungen und User-Feedback im Logbuch dokumentieren.

## Ergebnis
- Die Wiedergabe von Chrome-kompatiblen Videos wird beschleunigt und ressourcenschonender.
- VLC Pipe wird nur noch für wirklich inkompatible Formate genutzt.

---

*Letzte Änderung: 2026-03-15*
