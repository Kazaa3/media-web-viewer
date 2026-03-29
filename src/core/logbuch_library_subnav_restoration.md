# Logbuch: Library Sub-Navigation Tab Restoration

## Datum: 2026-03-29

### Kontext
- Ziel: Wiederherstellung und Modernisierung der Sub-Navigation im Bibliotheken-Tab (Library) für alle Medien-View-Modi.

---

## Umsetzungsschritte

### 1. View Switcher Restoration [GUI]
- 7 dedizierte Navigationsbuttons im `coverflow-library-panel` von web/app.html re-integriert.
- Buttons waren zuvor durch UI-Degradation verschwunden oder versteckt.

**Wiederhergestellte Views:**
- Coverflow: Immersive 3D-Navigation
- Grid: Standard-Medienraster
- Details: Listen-/Tabellenansicht
- Streaming: Video-Streaming-Layout
- Alben: Audio-Albumraster
- Folge ich: Gefolgte Inhalte
- Datenbank: Master-DB-Ansicht mit Such-/Importtools

### 2. UI-Konsistenz & Ästhetik
- Alle Buttons nutzen `.options-subtab` für konsistentes Styling (analog zu Debug, Parser, Reporting).
- Responsive SVG-Icons (Video, Audio, Playlist etc.) für bessere Scannability und Barrierefreiheit.
- Flex-Row-Container `#lib-nav-views-container` mit klarer Trennung zu Kategorie-Filtern.

---

## Verifikation

### Automatisierter Audit
- Navigationstrigger korrekt zu bestehenden Views gemappt:
  - Beispiel: `switchLibrarySubTab('grid')` → [JS-NAV] [SUBTAB-LIB] grid
- Trotz temporärer Verzögerung durch alte Hintergrundprozesse wurde die Trigger-Logik und Button-IDs in web/app.html bestätigt.

### Manueller UI-Audit
- Navigationszeile am oberen Rand des Library-Tabs sichtbar:

| Tab Name   | Trigger Function                  | Icon         |
|------------|-----------------------------------|--------------|
| Coverflow  | switchLibrarySubTab('coverflow')  | Columns/3D   |
| Grid       | switchLibrarySubTab('grid')       | Square Grid  |
| Details    | switchLibrarySubTab('details')    | Bullet List  |
| Streaming  | switchLibrarySubTab('streaming')  | Play Poly    |
| Alben      | switchLibrarySubTab('albums')      | Album Grid   |
| Folge ich  | switchLibrarySubTab('followed')   | User/Follow  |
| Datenbank  | switchLibrarySubTab('database')   | DB/Storage   |

---

## Maintenance Notes
- Active State: `switchLibrarySubTab` setzt `.active`-Klasse für neue Buttons automatisch.
- Modals: Modal-Transitions aus diesen Views nutzen weiterhin den zentralen `toggleModal`-Helper.

---

## Status
- Sub-Navigation und Views im Library-Tab sind vollständig wiederhergestellt und stabil.
- UI ist konsistent, barrierefrei und nachvollziehbar instrumentiert.
