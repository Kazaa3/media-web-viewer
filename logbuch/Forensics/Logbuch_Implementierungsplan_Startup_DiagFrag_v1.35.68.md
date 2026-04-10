# Logbuch: Implementierungsplan – Startup-Optimierung & Diagnostic Frag-Control (v1.35.68)

## Zielsetzung

- **Startup beschleunigen:** Blockierende Hardware- und Paket-Erkennung wird in einen Hintergrund-Thread verschoben. Die "Driver"- und "Env"-Tabs zeigen initial ggf. "Discovering...".
- **Granulare UI-Steuerung:** Neue technische Kontrolloberfläche (CFG-Tab) in der Diagnostics Sidebar für Feature-Toggles.

---

## Geplante Änderungen

### 1. Backend-Optimierung (Startup Speed)
- **config_master.py**
  - `hardware_info` und `installed_packages` werden auf Lazy-Loading/Deferred-Pattern umgestellt.
  - `background_version_discovery` befüllt diese Felder asynchron.
  - Platzhalter wie "Discovering..." verhindern Blockieren beim Import.
- **hardware_detector.py**
  - `get_gpu_info` nutzt kürzere Timeouts für `ffmpeg -encoders` oder überspringt, falls Binary nicht sofort gefunden.

### 2. Diagnostics UI Enhancement (Frag-Control)
- **diagnostics_sidebar.html**
  - [NEU] CFG-Tab-Button in der Sidebar.
  - [NEU] `diag-pane-config` mit Grid aus Toggle-Switches für Module & UI-Fragmente.
- **ui_nav_helpers.js**
  - `renderConfigToggles()` baut die Toggle-Liste dynamisch aus `window.CONFIG.ui_settings`.
  - Event-Listener rufen `eel.set_ui_setting` und triggern `refreshUIVisibility()`.
  - Zentralisierung der Sidebar-/Queue-Logik zur Vermeidung von Interferenzen.
- **audioplayer.js**
  - Refaktorierung: Direkte DOM-Manipulationen werden durch zentrale Helper ersetzt.

### 3. Fehlerbehebung ("Kreuzwirkung")
- **app_core.js**
  - Boot-Sequenz prüfen, damit Fragmente vor dem ersten `refreshUIVisibility` geladen sind.

---

## Offene Fragen
- **Persistenz:** Sollen UI-Toggles aus dem Diagnostics-Tab in einer .json gespeichert werden (persistente Konfiguration) oder nur für die Session gelten?
- **Sidebar-Typisierung:** "Detailed Sidebar" im Player als "Functional Module" oder "UI Fragment"? (Aktuell: Functional.)

---

## Verifizierungsplan

### Automatisierte Tests
- `src/core/config_master.py` direkt ausführen: Importzeit < 100ms.
- `eel.get_ui_settings` via Testscript triggern: Lazy-Felder werden nachgeladen.

### Manuelle Verifikation
- App starten, Sidebar ist sofort eingeklappt.
- Diagnostics → CFG-Tab: "Player"-Fragment toggeln, Nav-Button verschwindet/erscheint.
- "detailed-sidebar" toggeln: Öffnet/schließt im Player-View ohne Glitches.

---

**Review erforderlich:**
Bitte Feedback geben, insbesondere zur Persistenz der UI-Toggles.
