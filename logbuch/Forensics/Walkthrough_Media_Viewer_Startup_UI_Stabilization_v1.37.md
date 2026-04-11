# Walkthrough - Media Viewer v1.37 Startup & UI Stabilization

## Zusammenfassung
Die Startup-Sequenz und UI-Architektur des Media Viewer v1.37 wurden stabilisiert. Die Umgebung wird jetzt strikt verwaltet, um Prozesskonflikte zu verhindern, und das User Interface folgt einem klaren, vorhersehbaren Layout.

---

## Key Implementation Details

### 1. Robust Startup Sanitization
- **Prozessbereinigung:** Pfadbewusste Cleanup-Logik in `src/core/main.py` integriert. Beim Start werden automatisch:
  - Stale Player-Instanzen (basierend auf Projektverzeichnis) beendet
  - Zombie-Prozesse (ffmpeg, chromium) entfernt
  - Blockierte Ports (8345) mit einem Port-Harvesting-Tool freigegeben
- **Konfigurierbar:** Verhalten über `GLOBAL_CONFIG['ui_settings']['kill_on_startup']` steuerbar.

### 2. Persistent Navigation Architecture
- **Black Screen/Missing Sub-Menu Fix:** Kritische Navigationselemente wurden in das statische Shell verschoben:
  - **[GUI] TOP MENU BAR:** Immer sichtbar (Index Row 0)
  - **[GUI] SUB-MENU BAR:** Erzwingt `display: flex !important` und `opacity: 1`, sofort gerendert für schnellen Zugriff auf Queue, Playlist, Lyrics
  - **[GUI] AUDIO PLAYER FOOTER:** Fixiert am unteren Rand mit technischen Clustern für Echtzeit-Status

### 3. Authoritative UI Defaults
- **Sidebar:** Standardmäßig bei jedem Start ausgeblendet, um ein aufgeräumtes Interface zu gewährleisten. Alte localStorage-States werden durch die neue Boot-Sequenz überschrieben.
- **Global Visibility:** Alt-Key-Toggle-Logik aktualisiert, um versehentliches Ausblenden der Hauptsteuerung zu verhindern.

### 4. Structural Documentation
- **Explizite Kommentare** in `web/app.html` und `web/js/ui_nav_helpers.js` zur Definition der UI-Zonen:
  - `<!-- [GUI] TOP MENU BAR -->`
  - `<!-- [GUI] SUB-MENU BAR -->`
  - `<!-- [GUI] AUDIO PLAYER FOOTER -->`

---

## Verification Summary
- **Conflict Resolution:** `super_kill`-Logik in `main.py` aktiv
- **UI Parity:** Header und Sub-Navigation beim Start sichtbar
- **State Persistence:** Sidebar bleibt geschlossen, bis sie vom Nutzer geöffnet wird

Die Anwendung ist bereit für einen sauberen Neustart. Die Stabilität kann über das "Elite Technical HUD" im Header und Footer überprüft werden.
