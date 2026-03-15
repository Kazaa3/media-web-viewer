# Logbuch: Videoplayer-Optionen, Fallback & Teststrategie (2026-03-15)

**Datum:** 2026-03-15

## Änderungen & Hinweise
- Die FFmpeg-Option bleibt als alternative Abspielmöglichkeit im Backend erhalten und ist weiterhin testbar.
- MP4-Dateien werden im Fallback-Modus jetzt nicht mehr ausschließlich im Chrome Native Player, sondern auch über die Fallback-Logik (z.B. FFmpeg) gestartet.
- Die UI zeigt die FFmpeg-Option ggf. nur für fortgeschrittene Nutzer oder im Expertenmodus an.

## Teststrategie
### 1. Funktionale Tests
- **Test: MP4-Playback (Chrome Native & Fallback)**
  - Lade verschiedene MP4-Dateien (unterschiedliche Codecs, Bitraten, Container).
  - Prüfe, ob die Wiedergabe im Chrome Native Player und im Fallback (FFmpeg) jeweils funktioniert.
  - Prüfe Fehlerfälle (defekte MP4, nicht unterstützte Codecs).
- **Test: FFmpeg-Option sichtbar/nutzbar**
  - Stelle sicher, dass die FFmpeg-Option im UI (Expertenmodus) auswählbar bleibt.
  - Prüfe, ob der Backend-Call korrekt ausgelöst wird.

### 2. Performance-Tests
- **Test: Startzeit Wiedergabe (Chrome vs. FFmpeg)**
  - Messe die Zeit vom Klick auf "Play" bis zum ersten Frame/Sound für beide Modi.
  - Teste mit kleinen und großen MP4-Dateien.
- **Test: Systemauslastung**
  - Überwache CPU/RAM während der Wiedergabe (insb. bei FFmpeg).
  - Prüfe, ob parallele Wiedergaben oder schnelle Wechsel zu Problemen führen.

### 3. Regressionstests
- **Test: Fallback bei Fehlern**
  - Simuliere Fehler im Chrome-Player (z.B. inkompatible Datei, gezielte Exception).
  - Prüfe, ob automatisch der Fallback (FFmpeg) genutzt wird und die Wiedergabe startet.
- **Test: UI-Optionen**
  - Prüfe, dass keine Option doppelt oder widersprüchlich angezeigt wird.

## Ergebnis
- Die FFmpeg-Option bleibt für fortgeschrittene Nutzung und Fehlerfälle erhalten.
- MP4-Playback ist robuster, da der Fallback greift.
- Die Teststrategie stellt Funktion, Performance und Fehlerbehandlung sicher.

---

*Letzte Änderung: 2026-03-15*
