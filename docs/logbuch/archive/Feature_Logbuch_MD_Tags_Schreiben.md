# Feature: Logbuch .md Tags Writing

## Ziel
Ermöglicht das Schreiben und Verwalten von benutzerdefinierten Tags in Logbuch-Markdown-Dateien zur besseren Strukturierung, Filterung und automatisierten Verarbeitung.

## Motivation
- Tags bieten eine schnelle Möglichkeit, Einträge zu kategorisieren (z.B. "Milestone", "Bug", "Feature", "Refactor").
- Erleichtert die Suche, Sortierung und Analyse von Logbuch-Inhalten.
- Ermöglicht automatisierte Auswertungen und Filter in Build- und CI-Prozessen.

## Funktionsweise
- Tags werden als spezielle Markdown-Blöcke oder Inline-Elemente definiert:
  - Beispiel Block: `:::tag Milestone :::`
  - Beispiel Inline: `[tag:Feature]`
- Der File Handler erkennt und verarbeitet diese Tags beim Einlesen und Schreiben.
- Tags können mehrfach pro Datei oder Eintrag verwendet werden.
- Duplikate werden erkannt und ggf. gemeldet.

## Syntax-Beispiele
```
:::tag Milestone :::
:::tag Bug :::
[tag:Feature]
[tag:Refactor]
```

## Implementierungsdetails
- Parser für .md-Dateien erweitert um Tag-Erkennung (RegEx, Block/Inline).
- Chronologische und thematische Sortierung nach Tags möglich.
- Tag-Duplikate werden beim Schreiben geprüft.
- Tags können im UI angezeigt und gefiltert werden.

## Verifikation
- Testfälle: Schreiben, Erkennen, Duplikate, Sortierung.
- Integration in Build/Test-Gate.

## Ausblick
- Erweiterung für Tag-Hierarchien und Tag-Gruppen.
- Export/Import von Tag-Statistiken.

---

**Letzte Änderung:** 12. März 2026
