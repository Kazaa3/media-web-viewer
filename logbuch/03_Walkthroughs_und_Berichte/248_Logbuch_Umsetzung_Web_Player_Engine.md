# Logbuch: Umsetzung – Integrierter Web-Player mit Engine-Auswahl

## Todo-Liste & Umsetzungsschritte

### 1. Player-Modus-Auswahl im Frontend
- Dropdown im Video-Tab für Engine-Auswahl (Chromium Native, VLC Integrated)
- Auswahl wird im UI persistent gespeichert (z. B. localStorage)

### 2. Backend-Streaming-Endpoint für VLC/FFmpeg
- Erweiterung der Bottle-API um einen Streaming-Endpunkt
- Echtzeit-Transcoding via FFmpeg/VLC für "VLC Integrated"-Modus

### 3. ISO-Handling für Web-Player
- Extraktion des Hauptfilms aus ISO via VLC/FFmpeg
- Streaming an den Web-Player

### 4. UI/UX Verbesserungen
- Wegfall von Drag-and-Drop
- Medienauswahl direkt über Sidebar
- Player-Zustand (Modus) wird persistent gespeichert

## Technische Hinweise
- Backend: Subprocess-Pipeline für FFmpeg/VLC, Fehlerbehandlung für Transcoding
- Frontend: Erweiterung von app.html, Unterstützung für adaptive Streams (HLS/mp4)
- ISO: Spezielle Behandlung, um Hauptfilm zu erkennen und zu streamen

## Hinweis: FFmpeg vs. MKVToolNix/MKVmerge für Direct Play

- Für Direct Play ist FFmpeg nicht zwingend erforderlich!
- **Primär:** MKVToolNix (insbesondere mkvmerge) wird als Remuxer genutzt, um Medien ohne Re-Encode in kompatible Container (MP4/MKV) zu überführen.
- **Vorteile:**
  - Null CPU-Last, keine Qualitätsverluste
  - Schnelle Batch-Remux für große Libraries
  - Kompatibel mit HTML5-Player und Browser-Direct Play
- **FFmpeg:** Wird nur benötigt, wenn Transcoding oder Fragmented MP4/HLS für komplexe Formate/Live-Streaming erforderlich ist.
- **Empfehlung:**
  - Für Direct Play: mkvmerge/MKVToolNix
  - Für Live-Transcoding/Streaming: FFmpeg

---

# Walkthrough – Integrated Web Player & Streaming

## Umsetzung & Features

### 1. Backend Streaming Engine
- `app_bottle.py`: Neuer `/video-stream/`-Route hinzugefügt
- FFmpeg liefert einen live, fragmentierten MP4-Stream
- Optimiert für niedrige Latenz (`-preset ultrafast`, `-tune zerolatency`)
- ISO/DVD-Support: Routing über FFmpeg oder nativen Fallback

### 2. Frontend Player Selection
- `app.html`: Player-Modus im Video-Tab wählbar
  - **Chrome Native:** Direkte Wiedergabe browser-kompatibler Formate
  - **VLC Integrated (Stream):** Live-Transcoding & Streaming für MKV, ISO, komplexe Formate
  - **VLC (External):** Externen VLC-Player starten für Spezialfälle

### 3. Localization & UI Polish
- `i18n.json`: Labels für neue Player-Modi (Deutsch/Englisch)
- Video Player UI: Verbesserte State-Handling & Platzhalter-Transitions

### Verification Results
- **FFmpeg:** libx264 verfügbar, Fragmented MP4 (frag_keyframe+empty_moov) für Chromium-Streaming
- **UI:** Player-Modus dynamisch umschaltbar, Routing je nach Modus

## Summary
Die App bietet jetzt ein professionelles, integriertes Medien-Erlebnis. Externe Fenster entfallen, komplexe Formate wie ISO/DVD werden direkt im Web-Interface gestreamt.
