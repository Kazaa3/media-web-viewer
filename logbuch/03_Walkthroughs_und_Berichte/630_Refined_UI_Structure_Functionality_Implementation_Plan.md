# Logbuch: Refined UI Structure & Functionality Implementation Plan

**Datum:** 17. März 2026

## Ziel
Umfassende UI-Fixes und Erweiterungen für die Tabs "Item", "File" und "Reporting" sowie Verbesserungen bei der Kategoriefilterung und Picture-in-Picture (PiP) Unterstützung.

---

## Geplante Änderungen

### 1. Tab Naming & Labels
**Ziel:** Tabs klar als "Item" und "File" (bzw. "Datei" auf Deutsch) benennen.
**Aktionen:**
- Update von `web/i18n.json`:
  - `nav_item`: "Item"
  - `nav_file`: "Datei" (DE) / "File" (EN)
- Sicherstellen, dass `web/app.html` die Keys `data-i18n="nav_item"` und `data-i18n="nav_file"` verwendet.

### 2. "File" Tab Layout (Split-Pane)
**Ziel:** 2/3-Verhältnis für File-Browser (oben) und 1/3 für Ordnernavigation (unten).
**Aktionen:**
- CSS-Anpassung in `web/app.html`:
  - `#browser-top-pane`: `flex: 2; height: auto;`
  - `#browser-bottom-pane`: `flex: 1; height: auto;`
  - Container: `height: 100%; display: flex; flex-direction: column;`

### 3. Reporting Tab Initialization
**Ziel:** Dashboard standardmäßig anzeigen, nicht leeres Fenster.
**Aktionen:**
- `switchReportingView('dashboard')`-Aufruf in die `switchTab('reporting', ...)`-Logik in `web/app.html` einfügen.

### 4. Library Category Filtering
**Ziel:** Filter für Audio, Video, Bilder in Coverflow reparieren.
**Aktionen:**
- `CATEGORY_GROUPS`-Mapping in `web/app.html` JS definieren (wie Backend `cat_map`).
- `renderLibrary` so anpassen, dass geprüft wird, ob die Kategorie eines Items zur gewählten Gruppe gehört (z.B. bei Filter "audio": `item.category` ist "Album", "Hörbuch" etc.).

### 5. Picture-in-Picture (PiP) Support
**Ziel:** PiP-Funktionalität für Videoplayer.
**Aktionen:**
- `<button class="pip-btn">` zu den Player-Controls hinzufügen.
- `togglePip()` in JS implementieren (nutzt `video.requestPictureInPicture()`).

---

## Verifikationsplan

### Automatisierte Tests
- Browser-Subagent prüft:
  - Tab-Beschriftungen
  - Split-Pane-Höhen
  - Reporting-Tab-Inhalt beim Laden
  - Filterlogik für Coverflow
  - Vorhandensein und Funktion der PiP-Schaltfläche

### Manuelle Verifikation
- Split-Pane-Größenänderung testen
- Zwischen Kategorien wechseln und Coverflow-Verhalten prüfen

---

**Kommentar:**
Alle Änderungen wurden nach Plan umgesetzt und getestet. (Ctrl+Alt+M)
