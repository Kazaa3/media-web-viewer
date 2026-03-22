<!-- Category: infrastructure -->
<!-- Title_DE: Logging-Modul statt print und True-Checks -->
<!-- Title_EN: Logging module instead of print and true-checks -->
<!-- Summary_DE: Umstellung von ad-hoc Ausgaben und booleschen Direktabfragen auf strukturiertes Logging -->
<!-- Summary_EN: Migration from ad-hoc output and boolean direct checks to structured logging -->
<!-- Status: completed -->
<!-- Date: 2026-03-09 -->

# Logging-Modul statt print und True-Checks

## Ziel
Technische Diagnostik sollte konsistent, filterbar und reproduzierbar sein. Direkte `print(...)`-Ausgaben und verstreute `if True`-artige Schalter erschweren Wartung und Analyse.

## Umsetzung
- Nutzung des zentralen Logging-Setups statt direkter Konsolenausgaben.
- Log-Ausgaben über klar definierte Logger-Namen/Kategorien.
- Debug-Ausgaben über Logging-Level und Flags steuerbar.
- Fokus auf semantische Logs (Kontext + Aktion + Ergebnis) statt unstrukturierter Textfragmente.

## Ergebnis
- Bessere Nachvollziehbarkeit im Terminal und in Log-Dateien.
- Einheitlicher Stil für Diagnose-Ausgaben im gesamten Projekt.
- Weniger Seiteneffekte durch temporäre Debug-Prints im Produktivpfad.

## Hinweis für neue Änderungen
- Keine neuen `print(...)`-Debugs in produktiven Pfaden.
- Für Diagnostik immer Logger + passendes Level (`debug`, `info`, `warning`, `error`) nutzen.
