# Logbuch: VLC/FFmpeg-Option im Videoplayer vorübergehend entfernt (2026-03-15)

**Datum:** 2026-03-15

## Änderung
- Die Option, Videos direkt per FFmpeg an VLC zu übergeben, wurde im Videoplayer-UI vorübergehend entfernt.
- Grund: Stabilitäts- und Kompatibilitätsprobleme, die zu unerwartetem Verhalten führten.
- Die Standardwiedergabe erfolgt weiterhin über den nativen Chrome-Player.

## Hinweise
- Die Backend-Logik für FFmpeg→VLC bleibt erhalten, ist aber im UI aktuell nicht auswählbar.
- Die Option kann nach Stabilisierung und weiteren Tests wieder aktiviert werden.

## Ergebnis
- Die UI ist für Endnutzer klarer und robuster.
- Keine Fehlbedienung oder unerwartete Player-Wechsel mehr möglich.

---

*Letzte Änderung: 2026-03-15*
