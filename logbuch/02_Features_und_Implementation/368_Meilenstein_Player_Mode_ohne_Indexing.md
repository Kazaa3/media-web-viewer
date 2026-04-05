# Logbuch-Eintrag: Meilenstein – Player Mode ohne Indexing

**Datum:** 13.03.2026  
**Autor:** Copilot

## Kontext
Im Rahmen des aktuellen Meilensteins soll ein spezieller Player Mode implementiert, der ohne Medienindexierung arbeitet. Ziel ist es, einen schnellen, ressourcenschonenden Wiedergabemodus bereitzustellen, bei dem Indexierungsprozesse und Datenbankoperationen deaktiviert oder optional sind.

## Features
- **Player Mode ohne Indexing:**
  - Medien können direkt abgespielt werden, ohne dass sie zuvor in die Datenbank oder den Index aufgenommen werden müssen.
  - Ideal für temporäre, einmalige oder externe Medienquellen.
- **Set Indextime:**
  - Optionale Einstellung zur Festlegung eines Zeitpunkts für spätere Indexierung (z.B. nach dem Abspielen oder im Hintergrund).
  - Ermöglicht flexible Workflows: Sofortige Wiedergabe, spätere Indexierung nach Bedarf.
- **Einstellungen:**
  - Konfigurierbare Optionen im UI/Backend, um Indexing zu deaktivieren oder zu verzögern.
  - Nutzer kann wählen, ob und wann Medien indexiert werden.

## Motivation
- Schneller Start und reduzierte Wartezeiten für Medienwiedergabe
- Weniger Ressourcenverbrauch bei großen oder temporären Medien
- Flexible Nutzungsszenarien (z.B. Streaming, externe Laufwerke)

## Technische Überlegungen
- Anpassung von Player- und Indexing-Logik im Backend
- UI-Optionen für Player Mode und Indextime
- Sicherstellung, dass keine unerwünschten DB-Operationen ausgelöst werden

## Nächste Schritte
- Erweiterung der Player-Logik um Indexing-Flags
- UI-Integration für Mode- und Indextime-Einstellungen
- Tests für Player Mode ohne Indexing
- Dokumentation und User Guide
- Watchdog / Polling

---

**Fazit:**
Der Player Mode ohne Indexing ermöglicht eine schnelle, flexible Medienwiedergabe und schafft die Basis für weitere Optimierungen im Umgang mit temporären und externen Medienquellen.
