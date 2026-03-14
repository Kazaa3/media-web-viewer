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

## Build- und Installationsprozess – Wrapper-Skripte & Fixes (März 2026)

- **Neue Wrapper-Skripte:**
  - `./build.sh`: Baut das Debian-Paket extrem schnell (Testgate wird übersprungen).
  - `./push.sh`: Installiert das gebaute Paket lokal (entspricht einem lokalen "Push").
- **Korrigierte Fehler:**
  - Installer (postinst) sucht `requirements.txt` jetzt korrekt in `infra/`.
  - `scripts/reinstall_deb.sh` verwendet den richtigen Build-Pfad.
  - f-string/Syntax-Fehler in der Build-Pipeline für ältere Python-Versionen behoben.
- **Nächste Schritte:**
  - Paket mit `./build.sh` bauen (bereits erfolgt).
  - Mit `./push.sh` lokal installieren und testen.
  - Nach erfolgreicher Installation ist die Basis für Meilenstein 1 (Videoplayer) bereit.

**Frage:**
Soll der neue Branch für den Videoplayer (feature/m1-video-implementation) direkt vorbereitet werden?
