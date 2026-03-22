# Logbuch: Coverflow Library & UI Refinements

**Datum:** 16. März 2026

## Änderungen & Verbesserungen

### Internationalisierung
- **i18n.json**
  - Neue Einträge für "File"-Tab und Coverflow-Filter hinzugefügt.
  - Subkategorien (Audiobooks, Podcasts, Albums) ergänzt.

### UI-Optimierung
- **app.html**
  - Bestehenden "Library"-Tab und Panel in "File" umbenannt.
  - Neuen "Library"-Tab und Panel für Coverflow-Ansicht hinzugefügt.
  - Coverflow-UI mit CSS 3D-Transforms und flexiblem Container implementiert.
  - Filtersteuerung (Kategorie & Subkategorie) im neuen Library-Tab integriert.
  - `switchTab` refaktoriert, um Coverflow-Tab zu unterstützen und Rendering zu triggern.
  - `renderLibraryCoverflow()` hinzugefügt: Holt Medien mit Cover und zeigt sie als Karussell an.
  - Filterlogik implementiert, um Coverflow-Ansicht dynamisch zu aktualisieren.

### Popup-Reduktion
- **app.html**
  - Redundante `showToast`- und `alert`-Aufrufe beim Start und Tab-Wechsel entfernt oder reduziert.
  - Nur kritische Fehler lösen Modals aus, Infos werden dezent angezeigt.

### Media-Support
- **app.html**
  - DVD-Ordnerstrukturen (Ordner mit .iso und Artwork) werden korrekt im Media Viewer behandelt.

---

## Verifikationsplan

### Automatisierte Tests
- `test_i18n_coverage.py`: Prüft, ob alle neuen Keys abgedeckt sind.
- `test_js_error_scan.py`: JS-Sicherheit prüfen.

### Manuelle Verifikation
- Zwischen Tabs wechseln, "File" und "Library"-Labels prüfen.
- Coverflow-Ansicht testen: Scrollen, Artwork prüfen.
- Filter (Audio, Video, Images) anwenden und Ansicht prüfen.
- Subkategorie-Filter (Audiobooks, Podcasts) testen.
- Übermäßige Popups beim Navigieren und Start prüfen.
- Test mit "dvd folder test"-Struktur durchführen.

---

Weitere Details siehe vorherige Logbuch-Einträge und walkthrough.md.
