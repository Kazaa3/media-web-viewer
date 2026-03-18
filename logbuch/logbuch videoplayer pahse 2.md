# Projekt Logbuch: Media Web Viewer

## Aktueller Stand (18. März 2026)

### Fokus: Video Player Overhaul & Real-World Testing

Wir befinden uns in Phase 2 der Überarbeitung des Video-Players. Das Ziel ist die nahtlose Integration aller Formate (MP4, MKV, ISO) und Übertragungsarten (HLS, WebRTC, FragMP4).

### Offene Punkte & Status

| Punkt | Status | Beschreibung |
| :--- | :--- | :--- |
| **Port-Bindung (8345)** | ✅ Erledigt | Port 8345 ist nun Standard; Fallback auf dynamisch wenn belegt. Tests angepasst. |
| **VLC Prozess-Management** | ✅ Erledigt | `stop_vlc` killt nun zuverlässig auch externe Subprozesse. |
| **MP4 Ordner Playback** | ✅ Erledigt | `resolve_dvd_bundle_path` findet nun MP4-Dateien in Ordnern. |
| **mkvmerge Integration** | ✅ Erledigt | Standalone Integration für MKV-Remuxing (PIPE-KIT) aktiv. |
| **Advanced Tools UI** | ✅ Erledigt | Sub-Tabs (General, Tools, Environment) und Layout-Fix aktiv. |
| **Reporting Tab** | ✅ Erledigt | Parser-Performance Metriken und Verlaufs-Tabelle implementiert. |
| **m4p Black Screen** | ❌ Bekannt | `m4p` Videos liefern Ton aber schwarzes Bild. |
| **WebRTC / WHEP Support** | ⏳ Offen | Video.js Integration für sub-100ms Latenz via MediaMTX. |

### Nächste Schritte

1.  **Härtung der Transcoder-Logs**: Implementierung des Progress-Parsings in `transcoder.py`.
2.  **WebRTC Integration**: Frontend-Anpassung in `app.html` für WHEP.
3.  **End-to-End Verifizierung**: Durchführung der Selenium-Tests mit der realen MP4-Testdatei.

---
*Detaillierte Einträge finden sich in [docs/logbuch/](file:///home/xc/#Coding/gui_media_web_viewer/docs/logbuch/)*
