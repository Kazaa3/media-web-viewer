# Logbuch: Startup-Optimierung & Diagnostic UI-Expansion (v1.35.68)

## ✅ Zusammenfassung der Verbesserungen

### 1. Startup Performance Optimization
- **Deferred Discovery:**
  - Hardware- und Paket-Erkennung (I/O-intensive Tasks) laufen jetzt in einem Hintergrund-Thread (`background_version_discovery` in `config_master.py`).
- **Placeholder-First Boot:**
  - Die App initialisiert mit leeren/teilweisen Datenstrukturen, das Hauptfenster öffnet sofort, während Daten im Hintergrund geladen werden.
- **Hardware Detector Speedup:**
  - `get_gpu_info()` unterstützt jetzt `fast_mode` und setzt ein 2s-Timeout für Subprozess-Aufrufe, um den Start nicht zu blockieren.

### 2. Diagnostic "CFG" Tab
- **Granular Control:**
  - Neuer CFG-Tab in der Diagnostics Sidebar für Echtzeit-Toggles.
- **Functional Modules:**
  - Kern-Engines (Audio, Video, Queue, Lyrics) lassen sich live ein-/ausschalten.
- **UI Fragment Matrix:**
  - Sichtbarkeit einzelner UI-Komponenten (Sidebar, Navbars etc.) direkt steuerbar.
- **Backend Sync:**
  - Alle Toggles werden über `@eel.expose def set_ui_config_value` mit `GLOBAL_CONFIG` synchronisiert.

### 3. Centralized UI Visibility
- **Refined Orchestration:**
  - `refreshUIVisibility()` in `ui_nav_helpers.js` steuert jetzt granular die Sichtbarkeit von `player-detailed-sidebar` und `player-queue-list` anhand der neuen Flags.

---

## 🧪 Verifikationsergebnisse

### Startup Performance
- **Vorher:** Synchronous FFmpeg-Check und Version Discovery blockierten das Fenster für ~3-5s.
- **Nachher:** Fenster öffnet in <1s, Hardware-Infos erscheinen nach ~2s im TECHNICAL HUD.

### Functional Toggling
- **Audio Engine:** Umschalten funktioniert und wird mit `GLOBAL_CONFIG` synchronisiert.
- **Fragment Visibility:** Umschalten von `SIDEBAR_ALLOWED` oder `QUEUE_PANEL_ENABLED` aktualisiert die UI sofort ohne Reload.

---

## Technische Details
- **config_master.py:**
  - GLOBAL_CONFIG-Initialisierung refaktoriert, Deferred Discovery implementiert.
- **hardware_detector.py:**
  - `fast_mode` und 2s-Timeout für Subprozess-Aufrufe ergänzt.
- **ui_nav_helpers.js:**
  - `renderConfigToggles()` und `updateUIConfigToggle()` implementiert.
  - `refreshUIVisibility()` für granularen Player-Support erweitert.
- **CFG Tab:**
  - Neuer Reiter und Pane für Konfigurationsmanagement.

---

**Tipp:**
Nutze den CFG-Tab, um UI-Probleme zu debuggen oder schwere Module auf leistungsschwacher Hardware temporär zu deaktivieren – ohne .env oder config.json dauerhaft zu ändern.
