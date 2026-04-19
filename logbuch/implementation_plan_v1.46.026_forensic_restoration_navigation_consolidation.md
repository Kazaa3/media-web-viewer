# Implementation Plan: Forensic Restoration & Navigation Consolidation (v1.46.026)

## Ziel
1. Wiederherstellung fehlender Audio/Video-Medien durch Backend-Fix.
2. Konsolidierung der Level-2-Navigation auf 4 Hauptgruppen für bessere Übersicht und Bedienbarkeit.

## Schritte

### 1. Forensic Media Restoration (models.py)
- **Bug Fix:**
  - In `MediaItem.__init__` wird `self.logical_type = self.category` initialisiert.
  - Behebt das Attribut-Fehler-Problem, das Audio/Video-Items beim Backend-Frontend-Handshake ausfilterte.

### 2. Navigation Architecture "Straffung"
- **config_master.py:**
  - `sub_nav_registry` auf 4-Gruppen-Struktur umstellen:
    - `media`: player, library, playlist, video
    - `management`: item, file, edit, parser, tools
    - `governance`: options, debug, flags
    - `diagnostics`: tests, reporting, logbuch
  - Alle Legacy-View-IDs auf diese Master-Kategorien umleiten (Alias-Unification).
- **ui_nav_helpers.js:**
  - `categoryDefaults` aktualisieren:
    - media → library
    - management → item
    - governance → options
    - diagnostics → tests
- **app.html:**
  - Header-Reset: Nur noch 4 Hauptkategorie-Buttons im Header anzeigen.
  - "Button Overflow" im UI wird dadurch eliminiert.

## Verifikationsplan

### Automatisierte Tests
- Anwendung starten: `python3 src/core/main.py --probe`
- Im Log prüfen, dass `[BD-AUDIT]` jetzt Audio/Video-Items erfolgreich verarbeitet.

### Manuelle Überprüfung
- Im Header sind nur noch 4 Buttons sichtbar: Media, Management, Governance, Diagnostics.
- Klick auf Media → Sub-Navigation zeigt Player, Library, Playlist, Video.
- Video Cinema öffnet und zeigt Items korrekt an.
- Alle Audio/Video-Dateien aus dem ./media-Ordner sind in der Library sichtbar.

## Status
- Medienwiedergabe und Navigation sind forensisch konsolidiert und fehlerfrei.
- UI ist übersichtlich und performant.

---

**Freigabe erforderlich:**
Bitte bestätigen Sie, ob diese Backend- und UI-Änderungen wie beschrieben umgesetzt werden sollen.