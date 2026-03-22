# Logbuch Eintrag 019: Port-Binding Fixes und Video-Player Verfeinerung

## 📅 Datum: 2026-03-18
## 🚀 Status: In Bearbeitung / Teil-Implementiert

### 1. Port-Management & Stabilität
- **Problem**: Port 8080 war oft belegt, was zu Startfehlern oder Konflikten mit anderen Diensten führte. Selenium-Tests nutzten oft falsche URLs.
- **Lösung**: 
    - Umstellung auf **statischen Standard-Port 8345** (einzigartiger als 8080).
    - Persistenz des aktuell genutzten Ports in `src/parsers/.mwv_port` für externe Tools und Tests.
    - Automatisches Fallback auf dynamische Ports, falls 8345 belegt ist, mit entsprechender Warnung.
- **Resultat**: Zuverlässigerer App-Start und stabilere Test-Umgebung.

### 2. Video-Player Erweiterungen (Fixes)
- **Problem**: MP4-Dateien in Unterordnern ("Film-Objekt" Struktur) wurden nicht abgespielt; DVDs öffneten doppelte Fenster; Externe Player ließen sich nicht über die GUI beenden.
- **Lösung**:
    - **Intelligente Ordner-Auflösung**: `resolve_dvd_bundle_path` erkennt nun auch `.mp4`, `.mkv` etc. in Ordnern.
    - **Single-Popup Policy**: Routing für DVDs/ISOs korrigiert, um doppelte VLC-Instanzen zu vermeiden.
    - **Subprozess-Tracking**: Einführung von `ACTIVE_SUBPROCESSES` im Backend, um externe Player (VLC, mpv, ffplay) beim Klicken auf "Stop" in der GUI zuverlässig zu terminieren.
    - **UI-Feedback**: Anzeige eines dedizierten "Externer Player aktiv"-Status in der Video-Ansicht.

### 3. Offene Punkte (Backlog)
- [ ] Testlauf mit Real-World File: `Vortrag` (MP4).
- [ ] Gesamtheitliche Integration aller Formate und Übertragungsarten (HLS, WebRTC, FragMP4) im "Overhaul"-Modus prüfen.
- [ ] UI-Vervollständigung der Video-Steuerung (Timeline, Seek-Buttons etc. für alle Modi).

### 4. Nächste Schritte
1.  Verifizierung der MP4-Wiedergabe mit der realen Testdatei.
2.  Review der Transcoding-Pipeline für exotische Formate.
3.  Abschluss des Video-Player UI-Overhauls.
