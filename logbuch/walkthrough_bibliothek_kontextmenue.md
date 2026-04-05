# Walkthrough – Bibliothek-Fix & Kontextmenü-Implementierung

## Übersicht
Die Bibliothek wurde stabilisiert und ein globales Rechtsklick-Kontextmenü für alle Medienobjekte eingeführt.

---

## 1. Bibliothek-Stabilisierung
- **Zentralisierte Konstanten:**
  - `CATEGORY_MAP` wurde aus item.js nach common_helpers.js verschoben. Dadurch kann bibliothek.js Medienkategorien filtern und rendern, ohne abzustürzen.
- **Verbessertes Rendering:**
  - Alle Ansichten der Bibliothek (Coverflow, Grid, Datenbank, Details) erkennen und zeigen Medienobjekte jetzt korrekt an.

---

## 2. Globales Kontextmenü
- **Neues Utility:**
  - `showContextMenu(event, item)` wurde in common_helpers.js implementiert.
- **Dynamische Optionen:**
  - Das Menü bietet kontextabhängige Aktionen:
    - ▶️ Abspielen: Leitet das Objekt an den passenden Player weiter.
    - ➕ Warteschlange: Fügt das Objekt der aktiven Queue hinzu.
    - 📝 Metadaten Editieren: Öffnet das Objekt im Metadaten-Editor.
    - 📁 Im Dateisystem öffnen: (Eel-Integration) Öffnet den Ordner im Dateisystem.
- **Globale Integration:**
  - Das Kontextmenü ist aktiv in:
    - Der Bibliothek (alle Ansichten)
    - Der Audio-Queue (Player-Tab)
    - Dem Playlist-Manager

---

## 3. Strukturelle Anpassungen
- **app.html:**
  - Ein dedizierter `#context-menu`-Container wurde hinzugefügt, um das neue Menü zu unterstützen.
- **bibliothek.js:**
  - Native Rechtsklick-Events werden jetzt abgefangen und an das eigene Menü weitergeleitet.

---

## Verifikation
- **Bibliotheks-Integrität:**
  - Filterwechsel (Audio, Video, Film, Serie) führen nicht mehr zu Renderfehlern.
- **Kontextmenü-Sichtbarkeit:**
  - Rechtsklick auf ein Medienobjekt öffnet das Menü an der Mausposition.
- **Interaktion:**
  - Klick auf Menüoptionen (z.B. "Abspielen") führt die zugehörige Aktion korrekt aus.

---

**Tipp:**
Du kannst jetzt Medienobjekte effizienter verwalten, indem du sie per Rechtsklick zur Queue hinzufügst oder direkt im Metadaten-Editor öffnest.

---

**Siehe PR:** https://github.com/Kazaa3/media-web-viewer/pull/4
