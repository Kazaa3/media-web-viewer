# Logbuch: Videoplayer – Hybrid Fallback für MKV/Codec-Probleme (2026-03-15)

**Datum:** 2026-03-15

## Implementierte Änderungen
- **Hybrid Video Mode (Option 2):**
  - Die zweite Abspielstrategie heißt jetzt: "Chrome Native (mkvmerge/VLC Fallback)" (vormals "FFmpeg Engine → Chrome").
  - Im UI und in der internen Logik wird bei Auswahl dieser Option zuerst versucht, das Video nativ im Chrome-Player abzuspielen (maximale Performance).
  - Tritt ein Fehler auf (`onerror`-Event, z.B. bei nicht unterstützten Codecs wie MPEG-2/AC-3 in `abc.mkv`), erfolgt automatisch ein Fallback: mkvmerge → VLC Local Pipe.
- **Dateianalyse (`abc.mkv`):**
  - Datei enthält mpeg2video und ac3 – beides nicht von Chrome unterstützt.
  - Mit der neuen Logik wird nach Browser-Fehler direkt ein VLC-Remux gestartet, sodass die Datei trotzdem abspielbar ist.
- **Lokalisierung:**
  - `web/i18n.json` (de/en) angepasst: Option 2 beschreibt jetzt die neue Hybrid-Strategie technisch korrekt.

## Ergebnis
- Videos wie `abc.mkv` mit inkompatiblen Codecs werden nahtlos abgespielt: Erst Chrome Native, dann automatischer VLC-Fallback.
- Die UI und die technische Dokumentation spiegeln die neue Fähigkeit wider.
- Keine manuelle Umstellung oder Fehlermeldung mehr nötig – der Fallback ist vollautomatisch.

---

*Letzte Änderung: 2026-03-15*
