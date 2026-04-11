# Walkthrough - Master Geometry & Visibility Engine Overhaul (v1.37.52)

## Zusammenfassung
Die gesamte Geometry & Visibility Engine wurde grundlegend überarbeitet, um Black-Screen- und Sidebar-Overlay-Probleme zu beheben und ein dynamisches, pixelgenaues Interface zu gewährleisten.

---

## Technische Neuerungen

### Dynamische Offsets (Pixel-Perfekt)
- Globale Variable `--total-top-offset` berechnet die exakte Gesamthöhe:
  - Header sichtbar: +40px
  - Sub-Nav (Pills) sichtbar: +32px
  - Beide ausgeblendet: Offset = 0px, Content nutzt vollen Platz
- `main-split-container` nutzt jetzt `transition: var(--transition-fluid)`, um Layoutsprünge weich auszugleichen.

### Sidebar-Integration (v1.34 Elite)
- Sidebar-Breite wird über `--sidebar-width` gesteuert.
- Bei "ausgetoggelt" sofort 0px, Content füllt den Platz ohne Geisterränder.
- Sidebar ist standardmäßig geschlossen.

### Black-Screen Fix (Flex-Kollision)
- Kritischer Fehler in `.tab-split-layout` behoben:
  - Vorher: `flex-direction: row` → Untermenüs und Content nebeneinander, Viewport-Probleme
  - Jetzt: `flex-direction: column` → Header, Sub-Nav und Content sauber untereinander

---

## Was Sie jetzt sehen sollten
- **Beim Start:** Komplette schwarze Fläche ohne Sidebar (Elite Look)
- **Menüs:** Klick auf "Player" blendet Untermenüs (Queue/Lyrics) ein, Geometrie passt sich um exakt 72px (40+32) nach unten an
- **Header ausblenden:** Alles rutscht bündig nach oben

---

Bitte Anwendung neu laden und den globalen Toggle testen. Das Interface sollte jetzt stabil und dynamisch auf alle Sichtbarkeitsänderungen reagieren.