# Logbuch v1.37.51 – UI Category Refactor & True-All Filter

**Datum:** 2026-04-06

## Ziel
UI-Refactor der Kategorie-Filter im Player: Entfernung von "Multimedia", Einführung von "Video" und "Disk-Images", sowie ein wirklich inklusiver "Alle"-Filter.

## Maßnahmen & Änderungen

### 1. UI Refactor (Frontend Category Labels)
- **player_queue.html**
  - Dropdown: "multimedia" wird zu "video" umbenannt.
  - Neue Option: "Disk-Images (ISO/IMG)" als eigener Filter.
  - "Alle Medien (Komplette Bibliothek)" als erste und Standard-Option.

### 2. Filter Logic (Hydration)
- **audioplayer.js**
  - True-All-Logik: syncQueueWithLibrary ist bei "Alle"-Filter komplett permissiv, keine Medien werden mehr fälschlich ausgefiltert.
  - Kategorie-Synchronisierung: Neue Filter "video" und "disk_images" werden korrekt auf die Backend-IDs gemappt.

### 3. Backend & Migration
- (Bereits abgeschlossen: models.py refactored, db.py migriert, main.py bridges wiederhergestellt)

## Offene Frage
- Soll der "Alle"-Filter auch nicht abspielbare Items (z.B. .doc, .jpg) im Player anzeigen, wenn sie in der Bibliothek sind? (**Vorschlag:** Ja, für vollständige Diagnoseübersicht.)

## Verifikation
- **Manuell:**
  - Filterwechsel: "Video-Zweig" auswählen, nur Videos werden gelistet.
  - True-All: "Alle Medien" wählen, alle Musikstücke und Testvideos erscheinen.
  - Empty State: "Liste leeren" nutzen, Badge "0 Titel" aktualisiert sich sofort.

---
**Status:** UI-Filter-Refactor und True-All-Logik dokumentiert (v1.37.51)
