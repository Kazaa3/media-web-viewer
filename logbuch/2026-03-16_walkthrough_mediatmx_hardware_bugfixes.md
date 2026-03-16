# Walkthrough: MediaMTX, Hardware Detection & Bug Fixes

## Abschluss der Implementierungs- und Debugging-Phase
Alle geplanten Features sowie die gemeldeten Bugs wurden erfolgreich adressiert.

---

## 🚀 Neue Features

### MediaMTX Integration (HLS)
- **Backend:** Neuer Modus "mediamtx" in main.py integriert. Nutzt MediaMTX für hochperformantes Streaming.
- **Frontend:** hls.js Unterstützung für sub-100ms Seeking und native Browser-Wiedergabe.

### Hardware-Erkennung & Scan-Optimierung
- **Disk-Typ:** Automatische Erkennung von HDD vs. SSD/NVMe.
- **Anbindung:** Erkennung von PCIe Generationen und Netzwerk-Mounts (SMB/NFS).
- **Lightweight Mode:** Netzwerkpfade triggern automatisch einen ressourcenschonenden Scan, um I/O-Hangs zu vermeiden.

### Drag & Drop Playlist
- Medien-Items in der Bibliothek können nun intuitiv per Drag & Drop in die Playlist gezogen werden.

---

## 🐞 Behobene Fehler & UI Refinement

### Bug Fixes
- **Log-Level:** Unterstützung auf alle 4 Stufen + CRITICAL erweitert. Handler-Synchronisation im Backend korrigiert.
- **cats is not defined:** Die globale Variable cats wurde an den korrekten Scope verschoben, um Startup-Fehler zu vermeiden.
- **showToast is not defined:** Ein globaler Toast-Mechanismus wurde in app.html implementiert.
- **i18n.json Cleanup:** Dubletten und Syntaxfehler (fehlende Kommas) wurden bereinigt.

### UI Refinement
- **Transparente Modi:** Die Wiedergabe-Modi wurden exakt benannt:
  - ffmpeg mit cvlc (ehemals VLC hybrid)
  - mkvmerge mit cvlc
  - cvlc solo
  - Chrome Native
  - MediaMTX (HLS)

---

## 🛠️ Verifizierung
- **MediaMTX:** Erfolgreich getestet mit sub-100ms Seeking im Browser.
- **Log-Level:** Alle Stufen (DEBUG bis CRITICAL) werden korrekt im UI-Logbuffer und Terminal angezeigt.
- **Startup:** Keine JavaScript-Fehler mehr beim Laden der Anwendung (cats ist definiert).
- **Toasts:** VLC-Fallback und andere Benachrichtigungen erscheinen korrekt am unteren Bildschirmrand.
- **i18n:** Keine Dubletten-Warnungen mehr im Log.

---

## Toast Notification Demo
Schematische Darstellung: Toast erscheint bei VLC Fallback

---

## Kommentar
Ctrl+Alt+M

---

*Siehe logbuch/2026-03-16_walkthrough_advanced_playback_ui_debugging.md für vollständige Details und Proof of Work.*
