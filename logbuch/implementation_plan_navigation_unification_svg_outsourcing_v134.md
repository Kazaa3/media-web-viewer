# Implementation Plan – Navigation Unification & SVG Outsourcing (v1.34)

## Ziel
Cleanup und Konsolidierung der UI: Vereinheitlichung des Header-Systems und Auslagerung der SVG-Icons für bessere Wartbarkeit.

---

## Proposed Changes

### [Frontend] Asset Management
- **[NEW] icons.html**
  - Alle <symbol>-Definitionen (search, delete, edit, playlist, etc.) aus app.html extrahieren
  - Neue Datei: web/fragments/icons.html
- **[MODIFY] app.html**
  - Inline-<svg>-Block (ca. Zeile 135–238) entfernen
  - <div id="svg-icons-placeholder" style="display: none;"></div> ergänzen
  - Im DOMContentLoaded-Listener: FragmentLoader.load('svg-icons-placeholder', 'fragments/icons.html') aufrufen

### [Frontend] Navigation & Toggle Logic
- **[MODIFY] ui_nav_helpers.js**
  - toggleMenuBar():
    - #program-menu-bar und #sub-nav-container gemeinsam togglen (einheitlicher Boolean-State)
    - State in localStorage unter mwv_menu_system_visible speichern
    - headerHeight dynamisch berechnen: (mainVisible ? 40 : 0) + (subVisible ? 32 : 0)
  - switchMainCategory():
    - Sub-Navigation zeigt/versteckt sich automatisch, wenn Main-Bar sichtbar ist

### [Frontend] Styling
- **[MODIFY] web/css/main.css**
  - #sub-nav-container erhält transition: top 0.2s ease, opacity 0.2s ease (wie Main-Bar)

---

## Open Questions
- Soll die Sub-Navigation bei Kategorien ohne Sub-Items (z.B. File Browser) ausgeblendet werden oder als leerer Spacer sichtbar bleiben?
- Gewünschter "Handle"/Indikator für die Toggle-Bar im geschlossenen Zustand?

---

## Verification Plan
- **SVG Integrity:** Alle Icons (search, edit, volume, etc.) werden korrekt gerendert
- **Toggle Sync:** ALT-Taste toggelt beide Bars synchron
- **Margin Test:** Main-Content (Library, Player) wird nie "abgehackt", egal ob 1 oder 2 Bars aktiv sind
