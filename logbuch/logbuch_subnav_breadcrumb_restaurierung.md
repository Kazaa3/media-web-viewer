# Logbuch – Sub-Navigation & Breadcrumb-Restaurierung

## Datum
30. März 2026

## Ziel
Wiederherstellung der dynamischen Sub-Navigation (z.B. Player, Bibliothek, Playlist) nach Entfernung der alten Header. Einführung einer modernen, schlanken Breadcrumb-Navigation oberhalb des Hauptinhalts.

---

## Geplante/Umgesetzte Änderungen

### 1. Sub-Navigation
- **app.html:**
  - Das Element `<div id="sub-nav-container" class="sub-nav-bar">` wird wieder eingefügt.
  - Platzierung direkt am oberen Rand des Hauptinhaltsbereichs (`#main-content-area`).
- **Design:**
  - Die Sub-Navigation wird als schlanke Breadcrumb-Leiste gestaltet (ca. 40px Höhe, transparente oder leicht glasige Optik, abgerundete Buttons).
  - Die Hauptinhaltsfläche wird so angepasst, dass keine Überlappung mit der Sub-Navigation entsteht.

### 2. Navigation-Logik
- **ui_nav_helpers.js:**
  - Sicherstellen, dass `switchMainCategory` die Sub-Navigation korrekt anspricht.
  - Beim Wechsel der Hauptkategorie werden die relevanten Sub-Optionen automatisch in der Breadcrumb-Leiste angezeigt.

---

## Verifikation
- **Kategorie-Test:** Menü öffnen (ALT) → "Management" wählen → Sub-Buttons erscheinen oben.
- **Sub-Menü-Test:** Buttons wie "Item", "File", "Edit", "Parser", "Tools" erscheinen und funktionieren.
- **Fragment-Test:** Klick auf "Bibliothek" → interne View-Switcher (Grid, Details) bleiben funktionsfähig.

---

**Siehe PR:** https://github.com/Kazaa3/media-web-viewer/pull/4
