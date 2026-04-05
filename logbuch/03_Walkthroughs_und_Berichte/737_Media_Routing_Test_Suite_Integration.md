# 🧪 Test-Suite als Vorfilter für Media-Routing

In diesem Setup ist die „Test-Suite“ ein **Vorfilter**, der jede Datei vor dem Abspielen einmal kurz durch `ffprobe`/`FFmpeg` jagt, um über den optimalen Abspielpfad zu entscheiden: **Direct Play**, **HLS** oder **VLC**.

---

## 1. Was die Suite konkret tut

Für einen gegebenen Pfad (`full_path`):

1. **ffprobe-Analyse**  
   - Erkennt Container (mkv/mp4/iso), Dauer, Video-/Audio-Codecs, Auflösung, HDR-Flags, Untertitel und Kapitel.
2. **Kompatibilitäts-Check**  
   - Prüft, ob die Datei browsernatv (Direct Play) abspielbar ist (z. B. MP4 + H.264 + AAC).
3. **Quality-Score Berechnung**  
   - Berechnet einen Score basierend auf Auflösung (1080p/4K), Bitrate und technischer Ausstattung.
4. **Routing-Entscheidung**  
   - Wählt basierend auf dem Ergebnis den besten Modus (`direct`, `hls` oder `vlc`).

### Beispiel-Ergebnis (JSON):

```json
{
  "container": "matroska",
  "duration_min": 142.3,
  "video_codec": "hevc",
  "audio_codec": "truehd",
  "hdr": true,
  "subs": 2,
  "chapters": 24,
  "quality_score": 93,
  "direct_play_browser": false
}

---

## Implementation Plan

### Planning Phase
- Ziel: Integration und Test einer Media Routing Test Suite für automatisierte und manuelle Verifikation der Medienwiedergabe (Direct Play, HLS, VLC, ISO, MKV, Qualität).
- Aufgabenübersicht:
   - Implementierungsplan erstellen
   - Backend- und Frontend-Integration
   - Verifikation (automatisiert & manuell)

### Backend
- Implementiere `ffprobe_suite` und `quality_score` in `format_utils.py` (Analyse und Bewertung von Mediendateien)
- Implementiere `analyze_media` und `get_play_source` in `main.py` (Routing- und Analyse-Logik)
- ISO: Extrahiere Hauptfilm-Track (main movie) für ISOs
- MKV: Remux-to-MP4-Cache-Logik für schnelle Wiedergabe

### Frontend
- Aktualisiere `app.html` mit neuer Routing-Logik in `playItem`
- UI-Indikatoren für Quality Score und Playback Mode ergänzen

### Verification
- Erstelle und führe `/tmp/verify_routing_suite.py` aus (automatisierte Testfälle)
- Manuelle Verifikation der Wiedergabepfade (Direct, HLS, VLC)

---

## Execution Phase – Backend

### 1. ffprobe_suite & quality_score (`format_utils.py`)
- ffprobe-Auswertung für Streams, Bitrate, Auflösung, Codec, Container
- `quality_score`: Bewertet Medienqualität (z.B. Score 0–100)

### 2. analyze_media & get_play_source (`main.py`)
- `analyze_media`: Führt ffprobe-Analyse und Qualitätsbewertung durch
- `get_play_source`: Liefert optimalen Wiedergabepfad (Direct, HLS, VLC, Remux)

### 3. ISO Main Movie Extraction
- Logik zur Erkennung und Extraktion des Hauptfilms aus ISO-Images

### 4. MKV Remux-to-MP4 Cache
- Automatisches Remuxen von MKV zu MP4 für bessere Kompatibilität und Caching

---

## Execution Phase – Frontend

### 1. app.html Routing-Logik
- `playItem`-Funktion aktualisieren, um Routing-Entscheidungen des Backends zu nutzen

### 2. UI-Indikatoren
- Quality Score (z.B. als Badge, Farbe, Tooltip)
- Playback Mode (Direct, HLS, VLC) als Icon/Label

---

## Verification Phase

### 1. Automatisierte Tests
- `/tmp/verify_routing_suite.py` mit Testfällen für verschiedene Medientypen und Routen

### 2. Manuelle Verifikation
- Playback-Tests für Direct Play, HLS, VLC, ISO, Remux
- Überprüfung der UI-Indikatoren und Routing-Entscheidungen

---

## Lessons Learned / Hinweise
- Routing-Logik muss robust gegen fehlerhafte Metadaten und inkompatible Formate sein
- Caching und Remuxing können Performance und User Experience deutlich verbessern
- UI-Feedback (Score, Mode) erhöht Transparenz für den Nutzer

---

## Nächste Schritte
- Backend- und Frontend-Implementierung gemäß Plan
- Testfälle laufend erweitern und automatisieren
- Dokumentation und Lessons Learned ergänzen

---

## 2. Spezialfälle: MKV & ISO

### MKV → Direct-Play-Pfad
- Wenn die Codecs kompatibel sind, kann MKV über einen `/direct/` Endpunkt ausgeliefert werden (Progressive Download).
- Bei Inkompatibilität erfolgt ein Remux nach MP4 im Cache oder Fallback auf HLS.

### ISO → „Abspielbare Datei“
- Browser können keine ISOs laden. Die Suite extrahiert bei Bedarf automatisch die Hauptspur als MKV/MP4 in einen Cache, um sie anschließend über die normale Direct-Play/HLS-Pipeline abspielbar zu machen.

---

## 🧭 Routing-Strategie

Die Priorität liegt auf einer nahtlosen Browser-Integration:

1. **Direct Play (Native)**: Beste Qualität, keine Serverlast.
2. **HLS Streaming**: Hohe Kompatibilität, erfordert jedoch Transcoding/Remuxing.
3. **External Player (VLC)**: Ultimativer Fallback für komplexe Formate (HDR, PGS, TrueHD, ISO), die im Browser nicht perfekt darstellbar sind.

**Kurz gesagt:** Die Test-Suite liefert alle Informationen, die der Player benötigt, um „on-the-fly“ die richtige Abspieltechnologie zu wählen.
