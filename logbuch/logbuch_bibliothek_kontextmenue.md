# Logbuch – Bibliothek-Fix & Kontextmenü-Wiederherstellung

## Datum
30. März 2026

## Problemstellung
Die "Bibliothek"-Ansicht war nach der Modularisierung defekt und das Kontextmenü für Medienobjekte fehlte. Ursache war u.a. die fehlende globale Verfügbarkeit von `CATEGORY_MAP` und das Fehlen der Funktion `showContextMenu()` nach Refactoring.

---

## Geplante/Umgesetzte Änderungen

### 1. Zentrale Logik & Konstanten
- **common_helpers.js**:
  - `CATEGORY_MAP` wurde aus item.js ausgelagert und global verfügbar gemacht.
  - Die Funktion `showContextMenu(event, item)` wurde als globales Utility implementiert. Sie rendert ein schwebendes Menü an der Cursorposition.

### 2. Stabilisierung des Bibliothek-Moduls
- **bibliothek.js**:
  - Alle Renderer (Grid, Datenbank, Detail) setzen jetzt das Attribut `oncontextmenu` für Medienobjekte.
  - Interne Referenzen wurden korrigiert, sodass Sub-Tabs (Coverflow, Grid) wieder korrekt funktionieren.

### 3. Konsistenz der Fragmente
- **library_explorer.html**:
  - Alle benötigten Container-IDs (`coverflow-track`, `grid-container`) wurden geprüft und ggf. ergänzt.

---

## Verifikation
- **Bibliothek:** Coverflow- und Grid-Ansicht werden wieder korrekt mit Medienobjekten befüllt.
- **Kontextmenü:** Rechtsklick auf ein Objekt in Bibliothek, Audio-Queue oder Playlist öffnet ein Menü mit mindestens "Play" und "Edit".
- **Routing:** Auswahl von "Play" im Kontextmenü triggert korrekt den playMediaObject-Router.

---

**Siehe PR:** https://github.com/Kazaa3/media-web-viewer/pull/4
