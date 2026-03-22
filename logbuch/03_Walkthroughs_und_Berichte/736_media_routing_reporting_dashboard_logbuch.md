---

# Logbuch-Eintrag: Media Routing Test Suite & Reporting Dashboard Integration

## Überblick

Die Media Routing Test Suite und das Reporting Dashboard ermöglichen eine intelligente, automatisierte Analyse und Steuerung der Medienwiedergabe in deiner Mediathek. Sie bieten eine zentrale Übersicht über Kompatibilität, Qualität, Kategorien und Artwork-Status aller Medienobjekte.

---

## 1. Technische Analyse & Routing (Backend)
- **ffprobe_suite**: Tiefenanalyse (Codecs, Auflösung, HDR, Container, etc.)
- **ffprobe_quality_score**: Bewertet die technische Qualität (0–100)
- **is_direct_play_capable**: Prüft, ob Chrome/Browser das File direkt abspielen kann
- **analyze_media**: Eel-Endpoint für Analyse und Routing-Entscheidung
- **get_play_source**: Liefert optimalen Wiedergabepfad (Direct, HLS, VLC), inkl. ISO-Extraction und MKV-Remuxing
- **Neue Routen**: /direct/ und /cache/ für schnelle Auslieferung

---

## 2. Intelligentes Routing & Caching (main.py, app_bottle.py)
- Automatische Erkennung und Extraktion des Hauptfilms aus ISOs
- Remuxing von MKV zu MP4 für Direct Play im Browser
- Routing-Entscheidung: Direct (Browser), HLS (Transcode), VLC (Fallback)

---

## 3. Smartes Frontend-Routing & UI-Feedback (app.html)
- **playVideo** ruft die Test Suite auf und entscheidet den optimalen Pfad
- UI-Badges/Toasts für Quality Score und Playback Mode (Direct, HLS, VLC)
- Neue Filter und Kategorien für Filme, Serien, Alben, Podcasts, Soundtracks, Compilations, Playlists
- Chrome Native Badges (⚡ DIRECT) für 100% browserfähige Medien

---

## 4. Reporting Dashboard & Streaming Readiness
- "Routing Suite"-Tab mit:
  - Durchschnittlicher Quality Score
  - Direct-Play-Quote (Chrome Native)
  - Fallback-Statistiken (VLC/HLS)
  - Top-Qualität- und Problemdateien
  - Artwork-Health, Category-Distribution, Codec-Matrix
- Live-Performance-Metriken für Audio-Transcoding
- Inkompatible Inhalte werden mit Grund gelistet (z.B. Container/Codec)

---

## 5. Erweiterte Medienkategorisierung & Artwork-Logik
- Automatische Erkennung von Serien, Staffeln, Episoden, Alben, Compilations, Playlists
- Folder- und Tag-basierte Extraktion von Artist, Album, Jahr
- Artwork-Suche: Poster/Cover werden rekursiv in Parent-Foldern gesucht
- Neue UI-Filter für schnelle Navigation

---

## 6. Verifikation & Tests
- Automatisierte Tests: /tmp/verify_routing_suite.py und /tmp/verify_reporting_apis.py
- Manuelle Prüfung: Playback-Flows, UI-Badges, Reporting-Tab
- Statistiken und Health-Metriken werden im Dashboard angezeigt

---

## Fazit

Mit der Routing Test Suite und dem Reporting Dashboard erhältst du eine vollständige, automatisierte Übersicht über die technische Qualität, Kompatibilität und Kategorisierung deiner Mediathek. Playback-Entscheidungen, Artwork-Status und Streaming-Readiness sind jederzeit transparent und filterbar.
