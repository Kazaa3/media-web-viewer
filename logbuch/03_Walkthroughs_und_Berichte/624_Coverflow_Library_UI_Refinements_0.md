# Logbuch: Coverflow Library & UI Refinements 2.0

**Datum:** 16. März 2026

## Erweiterungen & Verbesserungen

### Internationalisierung
- **i18n.json**
  - Neue Einträge für "File"-Tab und Coverflow-Filter.
  - Subkategorien (Audiobooks, Podcasts, Albums) ergänzt.

### UI Expansion: Coverflow 2.0
- **3D-Depth:**
  - CSS `preserve-3d` und `transform: rotateY` für realistischeres Coverflow-Feeling verbessert.
- **Selection Highlighting:**
  - Visuelle Hervorhebung bei Fokus/Hover.
- **Smooth Navigation:**
  - Tastatur-Navigation (Pfeiltasten) für Coverflow implementiert.
- **Detailed Info Overlay:**
  - Overlay mit Metadaten (Jahr, Dauer, Codec) im Info-Panel.

### Testing Suite Expansion
- **Mock Layer:**
  - Unit-Tests mit simulierten Eel-Responses für schnelle UI-Logik-Validierung.
- **Real Layer:**
  - Integrationstests mit echten Dateien (ISO, DVD-Strukturen) für End-to-End-Prüfung.
- **test_coverflow_robustness.py:**
  - Zentrales Skript, das beide Layer orchestriert und DVD/ISO-Szenarien abdeckt.

### Media Support Refinement
- **DVD/ISO Detection:**
  - Scanner erkennt "DVD Folder Test"-Szenarien zuverlässig.
- **Artwork Association:**
  - poster.jpg/folder.jpg werden korrekt Coverflow-Items zugeordnet.

### Popup Reduction
- **app.html:**
  - Redundante `showToast`/`alert`-Aufrufe entfernt oder reduziert.
  - Nur kritische Fehler lösen Modals aus, Infos dezent angezeigt.

### Media Support
- **app.html:**
  - Media Viewer behandelt DVD-Ordnerstrukturen (inkl. Artwork) korrekt.

---

## Verifikationsplan

### Automatisierte Tests
- `test_i18n_coverage.py`: Neue Keys abgedeckt?
- `test_js_error_scan.py`: JS-Sicherheit?
- `test_coverflow_robustness.py`: Mock- & Real-Layer, DVD/ISO-Handling.

### Manuelle Verifikation
- Tabs wechseln, "File"/"Library"-Labels prüfen.
- Coverflow: Scrollen, Artwork, Tastatur-Navigation, Info-Overlay testen.
- Filter (Audio, Video, Images) und Subkategorien prüfen.
- Übermäßige Popups beim Navigieren und Start prüfen.
- "dvd folder test"-Struktur testen.

---

Weitere Details siehe vorherige Logbuch-Einträge und walkthrough.md.
