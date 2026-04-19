# Logbuch: Header Orchestration & Technical Overlay Steering

## Ziel
Die Steuerung von Header und technischen Overlays erfolgt jetzt vollständig konfigurationsgetrieben über `config_master.py`. Sichtbarkeit, Reihenfolge und Positionierung aller Navigationselemente sind granular steuerbar.

---

## Maßnahmen

### 1. Configuration Master (Backend)
- **config_master.py:**
  - Neues `header_registry` und `overlay_settings` im Block `ui_settings`:
    - `header_logo`: Sichtbarkeit und Text steuerbar.
    - `header_left_cluster`: Array von Action-Buttons (z.B. Exit, Power).
    - `header_mid_tabs`: Sortierbares Array von Tab-Objekten (Label, Route).
    - `header_right_cluster`: Einzel-Toggles für alle Buttons im rechten Cluster (Status, Sync, Swiss, DB, ...).
    - `technical_overlay`: Steuerung für das STABLE MODE-Badge (Sichtbarkeit, Position).

### 2. Header Orchestrator (Frontend)
- **app_core.js:**
  - `orchestrateHeaderUI()` implementiert:
    - Synchronisiert DOM mit `header_registry`.
    - Rendert Buttons bedingt nach Sichtbarkeits-Flags.
    - Sortiert Tabs dynamisch beim Bootstrap.

### 3. Nuclear Recovery Pulse
- **nuclear_recovery_pulse.js:**
  - `injectRecoveryBadge()` refaktoriert:
    - Respektiert `technical_overlay.visible`.
    - Setzt `top` und `right` Styles aus der Konfiguration.

### 4. Layout Restoration
- **app.html:**
  - IDs/Klassen zu Header-Clustern hinzugefügt, um chirurgische DOM-Manipulation durch den Orchestrator zu ermöglichen.

---

## Offene Fragen
- Sollen Buttons im rechten Cluster gruppiert werden (z.B. Diagnostics unter einem Master-Toggle) oder granular bleiben?
- Welche Aktionen sollen die neuen Left-Cluster-Buttons erhalten (z.B. Home, Refresh, Settings)?

---

## Verifikation
- **Automatisiert:**
  - Prüfen, ob `window.CONFIG.ui_settings.header_registry` nach Backend-Sync korrekt befüllt ist.
- **Manuell:**
  - Reihenfolge der Tabs in `config_master.py` ändern → UI sortiert Tabs neu.
  - Einzelne Buttons (z.B. DB Status) auf `False` setzen → Button verschwindet.
  - STABLE MODE-Badge über `top`-Konfiguration verschieben → Badge bewegt sich nach Reload.

---

*Status: Header- und Overlay-Steuerung vollständig konfigurationsgetrieben und flexibel. Weitere Feintuning-Optionen auf Wunsch möglich.*
