# Logbuch: mkvmerge-Integration & M4P/PIP-Probleme

## Stand März 2026

### mkvmerge-Integration
- **Status:**
  - mkvmerge wird für On-the-fly-Remux (Matroska) und als Streaming-Backend genutzt.
  - Aktuell fehlt eine eigenständige, dedizierte UI-Option für reines mkvmerge-Streaming (ohne VLC/FFmpeg).
- **ToDo:**
  - Eigenen Modus/Tab für mkvmerge-Streaming ergänzen.
  - Feedback/Status für mkvmerge-Operationen im UI anzeigen.
  - Testfälle für mkvmerge-only Routing anlegen.

### M4P/PIP-Playback-Probleme
- **Beobachtung:**
  - pip (Picture-in-Picture) funktioniert für M4P-Videos (Audio läuft, aber im Embedded Player bleibt das Bild schwarz).
  - Problem tritt nur im Embedded Player auf, nicht in externen Playern.
- **Analyse:**
  - M4P ist ein DRM-geschütztes Format (Apple FairPlay), wird von Browsern meist nicht nativ unterstützt.
  - Audio-Stream wird abgespielt, Video-Stream bleibt schwarz (fehlender Codec/DRM).
- **Workarounds:**
  - Externen Player (VLC, ffplay) für M4P erzwingen.
  - Im UI/Backend M4P-Dateien erkennen und Modus automatisch auf extern setzen.
  - Nutzerhinweis im UI anzeigen: "M4P kann im Browser nicht wiedergegeben werden. Bitte extern öffnen."

### Empfehlungen
- mkvmerge-Integration als eigenen Streaming-Modus sichtbar machen.
- Für M4P/PIP: Automatisches Routing auf externen Player, UI-Hinweis und ggf. Backend-Logik ergänzen.
- Testfälle für beide Szenarien anlegen.

---
Dieses Logbuch dokumentiert den Stand und die offenen Punkte zur mkvmerge-Integration sowie die bekannten Probleme mit M4P/PIP im Embedded Player.
