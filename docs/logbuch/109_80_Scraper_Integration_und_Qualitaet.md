<!-- Category: feature -->
<!-- Title_DE: Scraper Integration und Qualität -->
<!-- Title_EN: Scraper integration and quality -->
<!-- Summary_DE: Planung und Leitlinien für Scraper-Quellen, Mapping, Validierung und Fallback-Verhalten -->
<!-- Summary_EN: Plan and guidelines for scraper sources, mapping, validation, and fallback behavior -->
<!-- Status: planned -->
<!-- Date: 2026-03-09 -->

# Scraper Integration und Qualität

## Ziel
Externe Metadatenquellen sollen kontrolliert in die Medienbibliothek integriert werden, ohne lokale Datenqualität oder Stabilität zu gefährden.

## Scope
- Einbindung von Scraper-Quellen über ein klar definiertes Registry-/Provider-Modell
- Mapping externer Felder auf internes Datenmodell (Titel, Release, IDs, Cover, Genre)
- Prioritäts-/Trust-Regeln zwischen lokalen Parser-Daten und externen Scraper-Daten
- Saubere Fallback-Strategien bei fehlenden, widersprüchlichen oder fehlerhaften Antworten
- Nachvollziehbares Logging der Herkunft und Merge-Entscheidungen

## Qualitätsregeln
- Keine stillen Überschreibungen hochwertiger lokaler Metadaten
- Externe Daten nur bei ausreichender Qualität/Konsistenz übernehmen
- Konfliktfälle deterministisch und reproduzierbar auflösen
- Zeitlimits, Retry-Strategien und Error-Klassen pro Provider definieren

## Deliverables
- Einheitliche Scraper-Schnittstelle (Provider-API)
- Feld-Mapping und Normalisierungsschicht
- Validierungsregeln für kritische Felder (z. B. Jahr, Disc, Track, IDs)
- Testfälle für Happy-Path, Konflikte und Netzwerk-/Provider-Fehler
- Dokumentierte Betriebsregeln (Rate-Limits, Keys, Deaktivierung einzelner Provider)

## Akzeptanzkriterien
- Scraper-Ausfälle beeinträchtigen den lokalen Basisbetrieb nicht
- Merge-Ergebnisse sind konsistent und per Log nachvollziehbar
- Relevante Konfliktszenarien sind automatisiert getestet
- Provider können ohne Core-Refactor ergänzt/entfernt werden

## Abhängigkeiten
- Enge Kopplung mit Parser-Pipeline-Rework: [logbuch/15_Parser_Pipeline_Rework.md](logbuch/15_Parser_Pipeline_Rework.md)
- Nutzt M2-Datenmodell (Tags/Releases) als Zielstruktur für Anreicherung
