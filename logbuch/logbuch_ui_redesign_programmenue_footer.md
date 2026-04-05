# Logbuch – UI Redesign: Togglebares Programmenü & moderner Footer

## Datum
30. März 2026

## Ziel
Minimalistische Oberfläche durch Entfernung der klassischen Top-Navigation, Einführung eines togglebaren "Programmenüs" und Modernisierung der Fußleiste.

---

## Geplante/Umgesetzte Änderungen

### 1. Application Shell
- **app.html**:
  - Entfernung von top-bar (Zeilen 88–98) und layout-header (Zeilen 306–339).
  - Neuer Container `#program-menu-bar`, standardmäßig ausgeblendet.
  - Redesign des `#player-container` (Footer) mit runden, hochwertigen Buttons und Theme-Toggle.

### 2. Navigationslogik
- **ui_nav_helpers.js**:
  - Implementierung von `toggleMenuBar()` zum Anzeigen/Verstecken der neuen Menüleiste.
  - Sicherstellung, dass `switchMainCategory` korrekt über die neuen Menüeinträge funktioniert.

### 3. Styling
- **main.css**:
  - Styles für `#program-menu-bar` (schlankes, horizontales Menü).
  - Neue Klassen `.round-action-btn` und `.footer-glass`.
  - Anpassung des Layout-Containers, um den Platz der entfernten Header zu füllen.

---

## Verifikation
- **Menü-Toggle:** Das Programmenü erscheint/verschwindet auf Befehl (z.B. ALT-Taste oder Icon).
- **Kategorie-Navigation:** Alle 5 Hauptkategorien (Media, Video, Management, System, Diagnostics) sind über das Menü erreichbar.
- **Footer-Design:** Die Wiedergabebuttons sind rund und optisch konsistent.
- **Theme-Switch:** Der Theme-Toggle funktioniert an seiner neuen Position im Footer.

---

**Siehe PR:** https://github.com/Kazaa3/media-web-viewer/pull/4
