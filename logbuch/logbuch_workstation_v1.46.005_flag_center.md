# Logbuch: Forensic Workstation v1.46.005 – Global Flag Center (F2C)

## Datum
12. April 2026

## Zusammenfassung
Mit v1.46.005 wurde das Forensic Flag Center (F2C) eingeführt – ein zentrales Overlay zur Steuerung aller Sichtbarkeits- und Funktions-Flags der Workstation. Die Bedienung erfolgt in Echtzeit über ein konsolidiertes Dashboard im Footer.

## Wichtige Änderungen

### 1. System Registry & Configuration
- **config_master.py**:
  - MWV_VERSION auf v1.46.005 erhöht.
  - Alle enable_... und ..._visible-Flags in ein strukturiertes `UI_FLAG_REGISTRY` überführt.
  - Kategorien:
    - HUD & TECHNICAL: Diagnostics, Dom Auditor, Technical HUD, Sync Anchor
    - WORKSTATION SLOTS: Player, Library, Video, Edit Sidebars
    - CORE ENGINES: Audio Engine, Video Engine, Lyrics Panel
    - FOOTER CLUSTERS: DB Status, Swiss HUDs, Rescue Failover

### 2. Frontend Orchestration
- **forensic_flag_center.js** (neu):
  - Singleton-Pattern für Overlay-State
  - Dynamisches Rendering der Toggles basierend auf Registry
  - Event-Loop: `mwv-flag-update`-Events für Komponenten-Benachrichtigung
- **app.html**:
  - "FLAGS"-Button im Footer-Icon-Cluster injiziert
  - #forensic-flag-center Overlay-Container hinzugefügt

### 3. UI Styling & Aesthetics
- **main.css**:
  - Glassmorphes Styling für das Flag Center Overlay
  - High-Density-Toggle-Design
  - Utility-Klassen: `.mwv-flag-hidden`, `.mwv-flag-visible`

## Verifikationsplan
- **Automatisierte Tests:**
    - `python3 tests/forensic_hydration_check.py` (Backend-Logik prüfen)
    - `session.log` auf `[FLAG-PULSE]`-Traces prüfen
- **Manuelle Prüfung:**
    - "FLAGS"-Button im Footer klicken, Overlay erscheint
    - "Video Cinema"-Flag toggeln: Tab/Sidebar verschwindet/erscheint sofort
    - Nach Reload: Flag-States bleiben erhalten (Sync mit config_master.py)

## Status
- Flag Center (F2C) als zentrales Steuer-Overlay etabliert
- Echtzeit-UI-Pulsing und State-Persistenz gewährleistet
- System bereit für weitere Forensik- und UI-Evolution
