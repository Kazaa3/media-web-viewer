# Walkthrough - Dual Sub-Menu Conflict & UI Navigation Centralization (v1.37.03)

## Zusammenfassung
Der "Dual Sub-Menu"-Konflikt wurde gelöst, indem die Sichtbarkeitssteuerung der Navigationsleisten zentral in der globalen Konfiguration verwaltet wird. Die Oberfläche ist jetzt aufgeräumt und priorisiert das kompakte, professionelle Layout, während klassische Elemente weiterhin im Hintergrund verfügbar bleiben.

---

## 🛠️ Configuration & UI Restoration

### Centralized UI Settings (GLOBAL_CONFIG)
- Zwei neue, griffige Toggles in `src/core/config_master.py`:
  - `compact_pill_nav`: Die kleine, moderne Kontextleiste oben (standardmäßig AKTIV).
  - `integrated_tab_bar`: Die größere, modul-spezifische Tab-Leiste in der Mitte (standardmäßig INAKTIV, um Redundanz zu vermeiden).

### Dynamic Frontend Hydration
- In `web/js/ui_nav_helpers.js` wurde eine gehärtete Boot-Sequenz implementiert:
  - Beim Start holt das GUI die UI-Settings vom Backend.
  - Es setzt `display: none` für die große `integrated_tab_bar` und hält die `compact_pill_nav` immer sichtbar.
- Neue Backend-Endpunkte: `get_ui_settings` und `set_ui_setting` via Eel, damit Änderungen im Options-Panel direkt in die Konfiguration geschrieben werden.

---

## 📂 Structural Labels (v1.37.03)
- Explizite Code-Kommentare zur Unterscheidung der Bereiche:
  - `<!-- [GUI] COMPACT PILL NAV -->` (die kleine unter dem Header)
  - `<!-- [GUI] INTEGRATED TAB BAR -->` (die große in der Player-Ansicht)

---

## Empfehlung
Du kannst die Anwendung jetzt neu starten. Die große, redundante Tab-Leiste ist verschwunden, es bleibt nur die schlanke, kompakte Navigationsleiste oben.

---

**Betroffene Komponenten:**
- config_master.py
- main.py
- ui_nav_helpers.js
