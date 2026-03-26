# Architektur: Video Player & Media Routing

**Stand:** 26.03.2026

## Übersicht

Der Video Player ist als flexibles, modular erweiterbares System konzipiert, das verschiedene Medienquellen und Routen unterstützt. Die wichtigsten Komponenten und Routen sind:

### Hauptkomponenten
- **Frontend (web/app.html):**
  - Steuert das UI, Tab-Switching, Media-Detection und das Routing zu den passenden Player-Modi.
  - Unterstützt Direct Play, HLS, VLC, externe Player und Picture-in-Picture.
- **Backend (src/core/main.py):**
  - Stellt die API-Endpunkte für /direct/, /media-raw/, /video-stream/ bereit.
  - Orchestriert die Medienanalyse, Pfadauflösung und das Routing zu den passenden Engines (z.B. FFmpeg, VLC, native).
- **Test Suite (tests/unit/core/test_media_routing.py):**
  - Prüft die wichtigsten Media-Routen auf Erreichbarkeit und Fehlerfälle.

### Media Routing
- **/direct/**: Liefert Dateien direkt aus (z.B. MP4, WebM, MKV), bevorzugt für Browser-kompatible Formate.
- **/media-raw/**: Rohzugriff auf Medien, z.B. für spezielle Player oder Debugging.
- **/video-stream/**: Streaming-Route für transkodierte oder segmentierte Medien (HLS, FragMP4, etc.).

### Erweiterbarkeit
- Neue Engines und Routen können durch Ergänzen von Backend-APIs und UI-Buttons einfach integriert werden.
- Das Routing ist so gestaltet, dass neue Formate und Engines (z.B. WebRTC, MediaMTX) modular ergänzt werden können.

## Hinweise
- Die Architektur ist auf Robustheit und Fehlertoleranz ausgelegt (Fallbacks, Logging, Diagnose-Tools).
- Die Testabdeckung für Routing und Player-Integration wird kontinuierlich erweitert.

---

*Siehe auch: test_media_routing.py, app.html, main.py*
