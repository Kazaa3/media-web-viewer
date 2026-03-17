# Walkthrough – UI Refinement: Structure, Filtering & PiP

**Datum:** 17. März 2026

## Zusammenfassung
Zweite Runde der UI-Überarbeitung abgeschlossen: Struktur, Filterlogik und Picture-in-Picture (PiP) Funktionalität wurden wie gewünscht umgesetzt.

---

### 1. Tab Naming & Mapping Fixed
- Erster Tab: "Item", zweiter Tab: "File"
- Bug behoben, bei dem beide Tabs als "Item" angezeigt wurden (i18n-Mapping korrigiert)

### 2. "File" Tab Ratio (2/3 Split-Pane)
- Split-Pane-Layout im "File"-Tab angepasst
- Top Pane (File Browser): 2/3 der Höhe
- Bottom Pane (Library Folders): 1/3 der Höhe
- Splitter bleibt für manuelle Anpassung funktionsfähig

### 3. Reporting Tab Initialization
- "Reporting"-Tab zeigt beim Aktivieren standardmäßig das Dashboard an (kein leeres Fenster mehr)

### 4. Library Category Filtering Fixed
- Frontend `CATEGORY_MAP` implementiert, entspricht den Backend-Gruppen
- Hauptkategorie-Chips (Audio, Video, Bilder) filtern Coverflow und Grid jetzt korrekt (inkl. aller Subtypen)

### 5. Picture-in-Picture (PiP) Support
- PiP-Button (🖼️) zu den Video-Player-Controls hinzugefügt
- `togglePip()` implementiert: Video kann in ein schwebendes Fenster ausgelagert werden

---

## Verifikation
- Split-Pane-Ratio: Top ca. 62%, Bottom ca. 38% (flex 2:1)
- Reporting-Tab: Dashboard wird beim Aktivieren geladen
- Filter: Audio/Video/Bilder-Chips lösen korrekte Filterlogik aus
- PiP: Button vorhanden und funktionsfähig

---

## Nächste Schritte
- Verbesserungen am Core-Scanner zur besseren Erkennung/Kategorisierung (z.B. Dokumente, Spiele)
- Video-Player-Überarbeitung (später)

---

**UI Verification Recording:**
- Automatisierte und manuelle Tests durchgeführt, alle Kernfunktionen wie geplant umgesetzt und geprüft.
