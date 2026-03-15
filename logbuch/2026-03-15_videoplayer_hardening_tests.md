# Logbuch: Videoplayer – Optionen, Hybrid-Hardening & Test-Benchmarks (2026-03-15)

**Datum:** 2026-03-15

## Wichtige Verbesserungen

### 1. Playback-Optionen restrukturiert
- **Option 1:** Chrome Native (Standard-Browser-Playback)
- **Option 2:** FFmpeg Engine → Chrome (wiederhergestellte serverseitige Transkodierung)
- **Option 3:** Chrome Native (Hybrid VLC Fallback) – versucht natives Playback, fällt bei MEDIA_ERR_SRC_NOT_SUPPORTED (Code 4) automatisch auf mkvmerge/VLC-Pipe zurück

### 2. Hybrid-Logik gehärtet
- Fallback auf VLC wird **nur** bei MEDIA_ERR_SRC_NOT_SUPPORTED ausgelöst (nicht bei Netzwerk- oder Abbruchfehlern)
- Verhindert unnötige VLC-Starts bei großen, aber Chrome-kompatiblen MP4s

### 3. UI-Architektur verbessert
- `startEmbeddedVideo` unterstützt jetzt einen dedizierten `onErrorCallback` pro Modus
- Jeder Playback-Modus kann eigene Recovery-Strategien definieren, ohne globale Handler zu beeinflussen

### 4. Tests & Benchmarks
- **tests/test_video_performance_benchmark.py:** Misst Backend-Latenz für VLC-Pipe und Parser-Overhead
- **tests/test_video_modes_internal.py:** Prüft, dass alle internen Routen und Fähigkeiten vorhanden sind
- Alle Tests erfolgreich in `.venv_testbed` validiert

## Ergebnis & Verifikation
- `abc.mkv` kann mit Option 3 (Hybrid) nahtlos abgespielt werden: Chrome versucht nativ, erkennt inkompatiblen Codec und schaltet automatisch auf VLC um
- Standard-MP4s bleiben performant im Browser
- Playback-Architektur ist robuster, klarer und besser getestet

---

*Letzte Änderung: 2026-03-15*
