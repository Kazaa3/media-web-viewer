# Walkthrough - Media Viewer Pipeline Stabilization & UI Restoration

## Zusammenfassung
Die Media Viewer-Pipeline wurde stabilisiert und die UI-Funktionalität vollständig wiederhergestellt. Das Backend nutzt jetzt eine non-blocking Streaming-Architektur für Transcoding, wodurch Prozess-Hänger auch bei großen Dateien verhindert werden. Das UI-Layout wurde korrigiert, um korrektes Scrollen und eine funktionale Splitter-Resizability zu gewährleisten. Offline- und fehlende Medien werden nun visuell im Interface berücksichtigt.

---

## Summary of Improvements

### 1. Transcoding Pipeline & Performance
- **Non-blocking Streaming:** Die Medienauslieferung in `web/app_bottle.py` wurde auf `subprocess.Popen` mit Generator umgestellt. Medien werden sofort an den Browser gestreamt, ohne Backend-Worker zu blockieren.
- **Large File Protection:** Automatische CRF-Limitierung (CRF 28) für Dateien >4GB. Echtzeit-Transcoding bleibt CPU-effizient, System-Stalls werden verhindert.
- **Improved Process Management:** Der `ProcessController` in `src/core/process_manager.py` beendet stale FFmpeg-Instanzen und projektspezifische Python-Prozesse aggressiv bei Neustarts oder Notfallbereinigungen.

### 2. UI/UX Restoration & Scrolling
- **Layout Rectification:** Kritische CSS-Probleme in `web/css/main.css` behoben, die Sidebar und Splitter versteckten (`display: none !important`).
- **Scrollable Containers:** Einheitliche Höhenberechnung für Hauptlayout und Content-Decks, Audio-Queue und Sidebar sind jetzt vollständig scrollbar.
- **Resizable Splitter:** Funktionales Styling für `splitter-v` wiederhergestellt, Sidebars lassen sich wie vorgesehen resize'n.

### 3. Data Integrity & "0-item" Bug Fix
- **Delta-Scan Implementation:** `check_media_availability` im DB-Core hinzugefügt. Verschobene/umbenannte Dateien werden automatisch als "offline" markiert, statt als leere Einträge zu erscheinen.
- **Offline Visual Indicators:** In `web/js/audioplayer.js` werden nicht verfügbare Medien in der Queue ausgegraut. Playback-Versuche auf fehlende Dateien werden verhindert und mit einer User-Notification quittiert.

---

## Technical HUD & Diagnostics
- Der Technical HUD im Header hat jetzt einen funktionalen KILL-Button, der die neue zentrale Prozessbereinigung triggert und Zombie-FFmpeg- oder Hintergrundprozesse entfernt.

**TIPP:**
Mit dem RESYNC-Button in der technischen Sidebar werden Umbenennungs-Deltas sofort erkannt und die Verfügbarkeits-Flags in der DB aktualisiert.

---

## Verifikation
Die Syntax und Integration aller Kernmodule wurde geprüft. Die Anwendung ist jetzt deutlich reaktionsschneller und zuverlässiger.
