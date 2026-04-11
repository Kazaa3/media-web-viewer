# Implementation Plan – v1.34 UI Finalization & Media Pipeline Restoration

## Ziel
Behebung von UI-Inkonsistenzen im Footer, Aufteilung des Audio Players in Sub-Tabs und Wiederherstellung der echten Medienwiedergabe.

---

## Proposed Changes

### [UI] Layout & Navigation

**[MODIFY] app.html**
- Footer-Struktur aktualisieren:
  - **SCAN:** Startet vollständigen Filesystem-Scan (`scan(null, true)`).
  - **SYNC:** Synchronisiert Frontend und Backend (`refreshLibrary()`).
  - **RESET DB:** Initialisiert die Datenbank neu.
  - **THEME:** Theme-Toggle-Button in den Footer verschieben.
- Header/Subnav-Logik anpassen, um neue Audio Player Sub-Tabs zu unterstützen.

**[MODIFY] ui_nav_helpers.js**
- `switchMainCategory` generiert Sub-Tabs für Player:
  - Audio Player aufteilen in 'Warteschlange' und 'Mediengalerie' (v1.33-Stil).
  - **NEU:** Source Selection Dropdown in 'Mediengalerie' (Media Root, Library, Custom Path).
  - Wiederherstellung der 'Item Player'-Ansicht.
- Sidebar-Logik an neue Sub-Tabs anpassen.

---

### [JS] Audio Player & Item Gallery

**[MODIFY] audioplayer.js**
- **renderItemGallery():**
  - Repliziert die v1.33 Item Player View (links: Cover, rechts: vollständige Item-Liste).
- **Source Dropdown:**
  - In der Mediengalerie zwischen Root (./media), Library (DB) und Custom Path wählen.
- **Datenquellen:**
  - `allLibraryItems` für Galerie, `currentPlaylist` für Queue nutzen.

**[MODIFY] bibliothek.js**
- **loadLibrary:**
  - Logik fixen, damit echte Items nicht herausgefiltert werden.
  - Diagnostik-Logging verbessern, um Item-Fluss vom Backend zu verfolgen.

---

### [BACKEND] Data Synchronization

**[MODIFY] main.py**
- **get_library():**
  - Kategorie-Mapping an Parser-Ausgabe für echte Dateien anpassen.
- **scan_media:**
  - Stellt sicher, dass das Library-Ready-Event im Frontend ausgelöst wird.

---

## Verification Plan

### Automated Tests
- `python3.14 scripts/app_audit_playwright.py` prüft Tab-Switches und Button-Funktionalität.
- `logs/app.log` auf erfolgreiche Library-Fetch- und Filter-Meldungen überwachen.

### Manual Verification
- **Footer Check:** SCAN, SYNC und Theme-Toggle testen.
- **Player Check:** Zwischen "Warteschlange" und "Mediengalerie" wechseln, Rendering prüfen.
- **Data Check:** Echte Dateien in ./media/ erscheinen nach Scan in der "Mediengalerie".

---

**User Review Required:**
- Audio Player ist in Sub-Tabs aufgeteilt.
- Footer-Buttons und Theme-Toggle sind konsistent und funktional.
- Echte Medien werden nach Scan korrekt angezeigt und abgespielt.
