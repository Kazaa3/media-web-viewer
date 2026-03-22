# Problem: MPEG/H264-Container nicht abspielbar in VLC

**Datum:** 15.03.2026

## Fehlerbild
- Beim Versuch, ein Video im MPEG-Container mit H264-Codec im VLC-Modus abzuspielen, erscheint folgender Fehler:
  - `Codec 'h264' (H264 - MPEG-4 AVC (part 10)) is not supported.`
  - `VLC could not decode the format "h264" (H264 - MPEG-4 AVC (part 10))`
- Das Video wird nicht abgespielt.

## Analyse
- Die Fehlermeldung stammt direkt von VLC: Der installierte VLC-Build unterstützt den H264-Codec im MPEG-Container nicht.
- Ursache ist meist ein unvollständiger VLC-Build oder fehlende System-Codecs (z. B. auf minimalen Linux-Installationen).
- Das Problem betrifft ausschließlich den VLC-Modus. Andere Player-Modi (z. B. Chrome Native, FFmpeg Engine) können das Video ggf. abspielen.

## Lösungsvorschläge
- Prüfen, ob VLC mit allen relevanten Codecs installiert ist (z. B. Paket `vlc-full` oder zusätzliche Codec-Pakete).
- Alternativ das Video im "Chrome Native"-Modus oder mit "FFmpeg Engine" abspielen.
- Bei Bedarf VLC/Codecs nachinstallieren oder System-Codec-Support erweitern.

## Ergebnis
- Das Problem ist kein Bug der Anwendung, sondern ein Codec-/VLC-Installationsproblem.
- Die Anwendung erkennt und protokolliert den Fehler korrekt im Log.
