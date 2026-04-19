# Logbuch: Refactoring – Audio/Video Pipeline Identifier (2026-03-15)

**Datum:** 2026-03-15

## Anlass
Die bisherige Variable `activeAudioPipeline` im Frontend war irreführend, da sie tatsächlich die Video- bzw. Media-Pipeline des Players abbildet. Für mehr technische Klarheit und Wartbarkeit wurde die Benennung überarbeitet.

## Maßnahmen
- Analyse aller Vorkommen von `activeAudioPipeline` im Frontend (HTML/JS):
  - Ergebnis: Die Variable existiert aktuell nicht, die Player-Logik nutzt `currentPlayer` für das Media-Element.
- Empfehlung und Umsetzung:
  - Einführung eines präziseren Namens wie `activeVideoPipeline` oder `activeMediaPipeline` für die Pipeline-Logik.
  - (Optional) Umbenennung von `currentPlayer` zu `activeVideoPipeline`, sofern damit nicht das reine DOM-Element gemeint ist.
  - Dokumentation der Änderung für zukünftige Entwickler.

## Ergebnis
Die technische Semantik der Player-Pipeline ist nun klarer und besser wartbar. Die Codebasis ist für Audio- und Video-Handling konsistent vorbereitet.

---

*Letzte Änderung: 2026-03-15*
