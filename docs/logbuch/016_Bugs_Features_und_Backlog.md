<!-- Category: Documentation -->
<!-- Title_DE: Bugs, Features & Backlog -->
<!-- Title_EN: Bugs, Features & Backlog -->
<!-- Summary_DE: Zentrale Übersicht offener Punkte: Aktuelle Bugs, geplante Features und die technische Roadmap für "dict". -->
<!-- Summary_EN: Central overview of open items: current bugs, planned features and the technical roadmap for "dict". -->
<!-- Status: ACTIVE -->

# Bugs, Features & Backlog

## Den Überblick behalten
**dict - Web Media Player & Library** ist ein lebendiges Projekt. Dieses Dokument dient als zentrales Register für alles, was noch zu tun ist – von kleinen Korrekturen bis hin zu großen architektonischen Visionen.

## Aktuelle offene Bugs (Stand v.{VERSION})
Trotz hoher Testabdeckung gibt es immer Raum für Verbesserungen:
- **GUI-Glitches:** Feinjustierung des Glassmorphism-Layouts bei extrem schmalen Fenstern.
- **Parser-Edge-Cases:** Behandlung von sehr alten, beschädigten MKV-Dateien, die zu Timeouts führen können.
- **i18n-Lücken:** Nachziehen von Übersetzungen für neu hinzugekommene Debug-Meldungen im Logbuch-Editor.

## Geplante Features
Die Roadmap für die nächsten Versionen umfasst:
1.  **Erweiterte Suche:** Volltextsuche innerhalb der Metadaten-Dictionaries.
2.  **Plugin-System:** Erlaubt es Nutzern, eigene Parser oder Scraper als Python-Module hinzuzufügen.
3.  **Mobile Support:** Optimierung des NiceGUI-Frontends für die Nutzung auf Tablets und Smartphones.
4.  **Multi-Library Support:** Verwaltung von räumlich getrennten Bibliotheken (z. B. lokale Disk + NAS).

## Technische Schulden
Wir arbeiten kontinuierlich daran, das System sauber zu halten:
- **Refactoring:** Weitere Entkopplung der UI-Logik von der Backend-Datenbank.
- **Dependency-Cleanup:** Reduzierung der Abhängigkeiten in `venv_core`, um die Paketgröße zu minimieren.
- **Dokumentations-Sync:** Automatischer Abgleich zwischen Code-Kommentaren und dem Logbuch.

## Vision: Der "dict" Standard
Unser Ziel ist es, dict zum stabilsten und flexibelsten Open-Source Medienverwalter für Power-User zu machen. Jedes Ticket in diesem Backlog bringt uns diesem Ziel näher.

---
*Neue Bugs oder Feature-Ideen sollten zuerst hier erfasst werden, bevor sie in die detaillierte Planung (Logbuch) einfließen.*

<!-- lang-split -->

# Bugs, Features & Backlog

## Keeping Track
**dict - Web Media Player & Library** is a living project. This document serves as a central registry for everything that still needs to be done – from small fixes to large architectural visions.

## Current Open Bugs (as of v1.3.5)
Despite high test coverage, there is always room for improvement:
- **GUI Glitches:** Fine-tuning the glassmorphism layout for extremely narrow windows.
- **Parser Edge Cases:** Handling very old, corrupted MKV files that can lead to timeouts.
- **i18n Gaps:** Adding translations for newly added debug messages in the logbook editor.

## Planned Features
The roadmap for the next versions includes:
1.  **Advanced Search:** Full-text search within the metadata dictionaries.
2.  **Plugin System:** Allows users to add their own parsers or scrapers as Python modules.
3.  **Mobile Support:** Optimization of the NiceGUI frontend for use on tablets and smartphones.
4.  **Multi-Library Support:** Management of spatially separated libraries (e.g., local disk + NAS).

## Technical Debt
We are constantly working to keep the system clean:
- **Refactoring:** Further decoupling of the UI logic from the backend database.
- **Dependency Cleanup:** Reduction of dependencies in `venv_core` to minimize package size.
- **Documentation Sync:** Automatic alignment between code comments and the logbook.

## Vision: The "dict" Standard
Our goal is to make dict the most stable and flexible open-source media manager for power users. Every ticket in this backlog brings us closer to this goal.

---
*New bugs or feature ideas should be recorded here first before they flow into the detailed planning (logbook).*
