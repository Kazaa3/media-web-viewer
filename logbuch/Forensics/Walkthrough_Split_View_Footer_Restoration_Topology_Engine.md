# Walkthrough - Split View & Footer Restoration (Topology Engine)

## Zusammenfassung
Die Probleme "Missing Footer at Startup" und "Non-Adjustable Split View" wurden durch eine Neukalibrierung der Topology Engine und Splitter-Anker behoben.

---

## 🛠️ Restoration Log

### Split-View Restoration (Adjustable Geometry)
- Splitter Target IDs im Audio Player korrigiert: Der vertikale Splitter erkennt jetzt korrekt die `player-deck-column` (Artwork/Technik) und `player-playlist-column` (Queue) als Resize-Ziele.
- Splitter-Logik am `player-tab-split-container` verankert – ermöglicht "flüssige, pixelgenaue" Anpassung (Split einstellbar).

### Fast-Track Footer Hydration
- Sichtbarkeit des `layout-footer` durch expliziten Geometry-Pass im frühen DOM-Boot verstärkt.
- CSS-Variablen für Footer-Höhe werden sofort angewendet, sodass der Haupt-Viewport den Footer nicht mehr hinter den unteren Bildschirmrand schiebt.

### Boot Integrity
- `initAllSplitters()` und `refreshViewportLayout()` wurden in die Endphase des Logic-Bootstrappers (`ui_nav_helpers.js`) integriert.
- Die UI kennt jetzt ihre Dimensionen und interaktiven Grenzen, bevor der Nutzer das erste Mal klickt.

---

## How to verify
- **Split View:** Über der vertikalen Linie zwischen Artwork und Queue sollte der Cursor zu col-resize wechseln, die Spalten sind frei einstellbar.
- **Footer:** Die untere Diagnoseleiste (PID/BOOT/UP) erscheint jetzt zuverlässig beim Start, unabhängig vom aktiven Modul.
- Im Konsolen-Log erscheinen die Events als `[UI-NAV] REFRESH_GEOMETRY` während des Starts.
