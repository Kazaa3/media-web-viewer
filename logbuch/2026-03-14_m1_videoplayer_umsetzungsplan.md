# Meilenstein 1: Videoplayer – Umsetzungsplan (März 2026)

## Ziel
Implementierung eines stabilen, modernen Videoplayers als Kernfunktion für die Media Web Viewer App.

---

## 1. Branch-Setup
```bash
git checkout -b feature/m1-video-implementation
```

---

## 2. Backend (src/core/main.py)
- API-Endpunkt für Video-Streaming bereitstellen (z.B. `/api/video/<id>`)
- Unterstützung für verschiedene Videoformate (mp4, webm, mkv)
- Optional: Range-Requests für performantes Streaming
- Fehlerbehandlung (404, nicht unterstütztes Format)
- Logging für Zugriffe und Fehler

---

## 3. Frontend (web/app.html, web/app.js)
- Integration eines HTML5 `<video>`-Tags im UI
- Dynamisches Laden des Video-Streams via API
- UI-Controls:
  - Play/Pause-Button
  - Fortschrittsbalken (Seekbar)
  - Lautstärkeregelung
  - Optional: Vollbild, Zeitanzeige, Mute
- Fehleranzeige bei nicht unterstützten Formaten
- Responsive Design für Desktop und Tablet

---

## 4. Tests & Validierung
- Backend: Unit- und Integrationstests für Video-Endpunkt
- Frontend: UI-Tests (Play, Pause, Seek, Fehlerfälle)
- E2E-Test: Video wird geladen, abgespielt, Fehler werden korrekt angezeigt

---

## 5. Dokumentation & Logbuch
- Kurze Anleitung zur Nutzung des Videoplayers in DOCUMENTATION.md
- Logbuch-Eintrag zu Architekturentscheidungen und Lessons Learned

---

## 6. Ausblick
- Erweiterung um Playlist, Untertitel, verschiedene Audio-Tracks
- Performance-Optimierung (Buffering, adaptive Bitrate)
- Mobile-Support

---

**Startbereit: Sobald der Branch erstellt ist, kann die Umsetzung nach diesem Plan beginnen.**
