# Logbuch: Playlist-Item SVG-Icons – Status & ToDo

**Datum:** 2026-03-15

## Übersicht
Jedes Playlist-Item besitzt vier UI-Buttons, die als SVG-Icons umgesetzt werden sollen. Ziel ist eine konsistente, moderne und barrierefreie Bedienoberfläche.

---

## Aktueller Stand (2026-03-15)
- **Vorhandene Icons (bereits als SVG):**
  - **Move Up:** Pfeil nach oben (SVG, ersetzt 🔼)
  - **Move Down:** Pfeil nach unten (SVG, ersetzt 🔽)
- **Noch als Unicode/Font, SVG fehlt:**
  - **Grab/Drag-Handle:** ☰ (soll als SVG ersetzt werden)
  - **Remove/Delete:** ❌ (soll als SVG ersetzt werden)

## Zielzustand
- Alle vier Icons pro Item als SVG:
  1. **Grab/Drag-Handle:** Für Drag & Drop (SVG, z.B. "drag_indicator" oder "menu" aus Material Icons)
  2. **Move Up:** Pfeil nach oben (SVG, z.B. "arrow_upward" oder "swap_vert")
  3. **Move Down:** Pfeil nach unten (SVG, z.B. "arrow_downward" oder "swap_vert" rotiert)
  4. **Remove/Delete:** Löschen (SVG, z.B. "close" oder "delete" aus Material Icons)

## ToDo
- [ ] SVG für Grab/Drag-Handle integrieren (z.B. drag_indicator.svg)
- [ ] SVG für Remove/Delete integrieren (z.B. close.svg oder delete.svg)
- [x] SVG für Move Up integriert
- [x] SVG für Move Down integriert

## Hinweise
- Die Icons befinden sich im Ordner `web/icons/Google Fonts Material Icons/`.
- Die Integration erfolgt per CSS-Mask (siehe .icon-move-up, .icon-move-down etc.).
- Nach SVG-Integration: Test auf Barrierefreiheit und konsistente Darstellung in allen Browsern.

---

*Letzte Änderung: 2026-03-15*
