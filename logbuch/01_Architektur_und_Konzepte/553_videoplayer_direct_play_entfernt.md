# Logbuch: Videoplayer – Direct Play Option entfernt (2026-03-15)

**Datum:** 2026-03-15

## Änderung
- Die Option "Direct Play" wurde aus dem Videoplayer entfernt.
- Grund: Vereinfachung der Playback-Architektur und Vermeidung von Redundanz mit den bestehenden, technisch klareren Modi (Chrome Native, FFmpeg Engine, Hybrid VLC Fallback).
- Die Wiedergabe erfolgt jetzt ausschließlich über die drei Hauptoptionen, die alle relevanten Anwendungsfälle abdecken.

## Ergebnis
- Die UI ist übersichtlicher und weniger fehleranfällig.
- Die technische Wartung und Erweiterung der Playback-Logik wird erleichtert.

---

*Letzte Änderung: 2026-03-15*
