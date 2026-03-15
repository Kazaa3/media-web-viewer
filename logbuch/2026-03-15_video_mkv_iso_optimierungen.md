# Logbuch: Optimierungen für MKV/Videos und ISO-Dateien (2026-03-15)

**Datum:** 2026-03-15

## Ziel
- Performance- und Kompatibilitätsoptimierungen für das Abspielen und Verarbeiten von MKV-Videos und ISO-Images im Videoplayer.

## Optimierungsansätze
- **MKV-Handling:**
  - Es wird keine Engine grundsätzlich bevorzugt: FFmpeg, mkvmerge und cvlc werden je nach Dateityp, Fehlerfall und Performance-Test dynamisch eingesetzt.
  - Die Auswahl der Engine (FFmpeg, mkvmerge, cvlc) erfolgt nach Stabilität, Kompatibilität und Geschwindigkeit im jeweiligen Szenario.
  - Automatische Codec-Erkennung und ggf. Transkodierung, falls Chrome/VLC inkompatible Streams erkennt.
  - Fehlerhafte oder unvollständige MKV-Dateien werden frühzeitig erkannt und im UI als problematisch markiert.
- **ISO-Images:**
  - Unterstützung für DVD-ISOs über das native VLC-`dvd://`-Protokoll und cvlc (headless VLC).
  - ISO-Parsing kann wahlweise mit pyisolib oder anderen ISO-Parsern erfolgen – je nach Performance-Test und Kompatibilität.
  - Automatische Erkennung von ISO-Images und Auswahl des passenden Abspielmodus (z.B. VLC Pipe, Embedded VLC, cvlc).
  - Fortschrittsanzeige und Fehlerbehandlung bei nicht gemounteten oder beschädigten ISOs.
- **Allgemein:**
  - Logging und UI-Feedback für alle Fehlerfälle (z.B. "MKV beschädigt", "ISO nicht lesbar").
  - Performance-Messungen für Startzeit und Ressourcenverbrauch bei großen MKV/ISO-Dateien.

## Ergebnis
- Zuverlässigere und schnellere Wiedergabe von MKV- und ISO-Dateien.
- Bessere Fehlerdiagnose und Nutzerführung bei problematischen Medien.
- Grundlage für weitere Optimierungen (z.B. Hardware-Decoding, parallele Analyse von ISO-Strukturen).

---

*Letzte Änderung: 2026-03-15*
