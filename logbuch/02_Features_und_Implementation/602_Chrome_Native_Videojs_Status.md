# Logbuch: Chrome Native & Video.js Player-Status

**Datum:** 16. März 2026

## Statusüberprüfung: Chrome Native & Video.js

### Hintergrund

Im Rahmen der Player-Überarbeitung wurde festgelegt, dass der Modus "Chrome Native" für alle browserbasierten Wiedergaben (Direct Play, MediaMTX HLS/WebRTC, FFmpeg Browser) weiterhin Video.js als primären Player nutzt. Dies gewährleistet maximale Kompatibilität und einheitliches Verhalten im Browser.

### Überprüfung

- **Aktueller Stand:**
  - Chrome Native verwendet Video.js als Standardplayer für alle relevanten Modi.
  - Keine Abweichungen oder Umstellungen auf andere Player festgestellt.

- **Hinweis:**
  - Sollte Chrome Native zwischenzeitlich nicht mehr Video.js nutzen, ist dies rückgängig zu machen, um die ursprüngliche Strategie beizubehalten.

### Empfehlung

- Regelmäßige Überprüfung der Player-Zuordnung im Frontend (insbesondere in `app.html` und zugehörigen JS-Modulen).
- Bei Änderungen an der Player-Logik sicherstellen, dass Chrome Native immer Video.js verwendet.

---

Weitere Details siehe Implementation_Plan_Expanded_Playback_Mini_Video_Overlay.md.
