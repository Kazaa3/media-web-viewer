# Problem: MP4-Dateien werden nicht als Media-Items angezeigt

**Datum:** 15.03.2026

## Fehlerbild
- Dateien mit der Endung `.mp4` erscheinen nicht in der Medienübersicht bzw. werden nicht als Video-Items erkannt.

## Analyse
- Die Filterung für Video-Dateien erfolgt im Backend über die Konstante `VIDEO_EXTENSIONS` (in `src/parsers/format_utils.py`).
- Im Frontend ist `.mp4` in der Liste der unterstützten Video-Erweiterungen enthalten.
- Wenn `.mp4` im Backend nicht in `VIDEO_EXTENSIONS` enthalten ist, werden MP4-Dateien beim Scan/Import ignoriert.

## Lösung
- Prüfen, ob `.mp4` in der Konstante `VIDEO_EXTENSIONS` enthalten ist.
- Falls nicht, `.mp4` ergänzen, damit MP4-Dateien als Video erkannt und angezeigt werden.

## Ergebnis
- Nach Ergänzung von `.mp4` in `VIDEO_EXTENSIONS` werden MP4-Dateien korrekt als Video-Items erkannt und in der App angezeigt.
