# Logbuch v1.37.49 – Category Refactor, Port-Fix & Hydration Repair

**Datum:** 2026-04-06

## Ziel
Abschaffung der Kategorie "multimedia" zugunsten von "video" im gesamten Stack, Behebung von Port-Konflikten und Reparatur der Bibliothekshydration sowie der "Liste leeren"-Funktion.

## Maßnahmen & Änderungen

### 1. Environment Stabilization
- **Port-Freigabe:**
  - Mit `fuser -k` und `pkill` wird Port 8345 freigeräumt, damit die App fehlerfrei starten kann.
- **Backend Bridge:**
  - Fehlende Funktionen `db.get_library()` und `get_library_forensics()` in main.py wiederhergestellt, um Diagnostik und Overlay zu ermöglichen.

### 2. Category Mapping Overhaul (SSOT)
- **models.py**
  - MASTER_CAT_MAP: "multimedia" wird zu "video" umbenannt.
  - BRANCH_MAP: Nur noch "audio", "video", "disk_image" als Hauptzweige.
  - Alias-Logik: Alle Synonyme (Film, Serie, TV) werden auf "video" gemappt.
- **db.py**
  - Migration: Alle "multimedia"-Einträge in der DB werden zu "video" umbenannt.
  - API-Alias: `get_library = get_all_media` für interne Kompatibilität.

### 3. UI Logic Repairs
- **audioplayer.js**
  - "Liste leeren": clearQueue-Logik repariert, damit der Zustand im Frontend korrekt zurückgesetzt wird.
  - Hydration Sync: syncQueueWithLibrary auf "video"-Label abgestimmt, um Filterfehler zu vermeiden.
- **common_helpers.js**
  - isVideoItem erkennt jetzt das neue "video"-Label.

## Offene Frage
- Soll "Liste leeren" auch die Mock-Items im Bypass-Modus entfernen? (**Vorschlag:** Ja, für sofortiges Feedback.)

## Verifikation
- **Automatisiert:**
  - eel.get_allowed_internal_cats(['multimedia']) gibt jetzt ['video'] zurück.
- **Manuell:**
  - Diagnostics Overlay zeigt echte DB-Statistiken, kein "Audit Bridge Fault" mehr.
  - App startet ohne "Address already in use"-Fehler.
  - Die 3 Musikstücke erscheinen im Standard-View, wenn Bypass deaktiviert ist.

---
**Status:** Kategorie-Refactor, Port-Fix und Hydration-Logik erfolgreich dokumentiert (v1.37.49)
