# Anpassungen Debug & DB Tab – Media-Item-Ansicht, Dark Style, Konfigurationsmenü

**Datum:** 14.03.2026

## 1. Wiederherstellung der Media-Item-Ansicht
- Der Bereich "Python Dict (Details)" zeigt nun wieder standardmäßig die Liste der Medien-Einträge (MediaItem Dicts) an.
- Die Daten werden automatisch aktualisiert, wenn die Bibliothek geladen oder gescannt wird (sofern "Bibliothek" im Menü ausgewählt ist).

## 2. VS Code Dark Style
- Der violette Farbverlauf wurde entfernt.
- Das Design entspricht jetzt dem klassischen VS Code Dark Theme:
  - **Hintergrund:** #1e1e1e
  - **Rahmen:** Subtiles #333
  - **Syntax-Highlighting:**
    - Blau für Keys
    - Orange für Strings
    - Hellgrün für Zahlen

## 3. Neues Auswahl-Menü für Konfigurationen
- Oben rechts im Dict-Bereich befindet sich jetzt ein Dropdown-Menü.
- Umschaltbare Ansichten:
  - **Bibliothek (Media Items):** Liste der indexierten Dateien (Standard)
  - **Parser Konfiguration:** Aktuelle Einstellungen der Parser-Chain
  - **System Umgebung:** Python-Version, Pfade, PIDs und OS-Infos
  - **Debug Flags:** Status aller internen Debug-Schalter
- Die Lokalisierung (Deutsch/Englisch) für das neue Menü wurde in die `i18n.json` eingearbeitet.

---

**Ergebnis:**
- Die Media-Item-Ansicht ist wieder intuitiv nutzbar.
- Das UI ist konsistent im VS Code Dark Style gehalten.
- Das neue Konfigurationsmenü ermöglicht schnellen Wechsel zwischen wichtigen Ansichten und ist mehrsprachig verfügbar.
