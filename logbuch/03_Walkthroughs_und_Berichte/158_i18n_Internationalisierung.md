<!-- Category: feature -->
<!-- Title_DE: i18n Internationalisierung -->
<!-- Title_EN: i18n internationalization -->
<!-- Summary_DE: Leitlinien und nächste Schritte zur nachhaltigen Internationalisierung über UI, Logbuch und Runtime-Texte -->
<!-- Summary_EN: Guidelines and next steps for sustainable internationalization across UI, logbook, and runtime texts -->
<!-- Status: active -->
<!-- Date: 2026-03-09 -->

# i18n Internationalisierung

## Ziel
Die Internationalisierung wird dauerhaft als Qualitätskriterium im Entwicklungsfluss verankert.

## Fokus
- Konsistente DE/EN-Key-Parität in `web/i18n.json`
- Keine neuen hardcodierten UI-Strings in HTML/JS
- Einheitliche Benennung und Struktur von i18n-Keys
- Saubere Trennung zwischen UI-Texten und internen Log-/Debug-Ausgaben

## Umsetzungslinien
- Neue UI-Texte nur über i18n-Keys (`data-i18n`, `t('...')`)
- Fehlende Key-Paare sofort im selben Commit ergänzen
- Bestehende Dialog-, Fehler- und Statusmeldungen schrittweise harmonisieren
- Tests als Gate nutzen, damit i18n-Regressionen früh sichtbar sind

## Deliverables
- Bereinigte und konsistente Key-Struktur in `web/i18n.json`
- Checkliste für i18n bei neuen Features/PRs
- Nachgezogene Übersetzungen für offene Randfälle in UI und Logbuch-bezogenen Views

## Akzeptanzkriterien
- DE/EN sind für aktive UI-Flows vollständig verfügbar
- Keine neuen Hardcoded-Texte in produktiven UI-Pfaden
- i18n-Tests laufen stabil in der Standard-Testausführung

## Bezug
- Historischer Abschlussstand: [logbuch/41_Internationalization.md](logbuch/41_Internationalization.md)
- Unterstützt M3 (GUI) und M4 (Qualität/Release) durch sprachkonsistente UX
