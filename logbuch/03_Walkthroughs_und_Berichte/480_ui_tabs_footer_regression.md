# UI-Regression: Tabs & Footer-Layout defekt

**Datum:** 15.03.2026

## Problem
- Nach den letzten UI-Änderungen sind alle Tabs im Layout "zerschoßen" (fehlerhaft dargestellt).
- Der Footer ist nicht mehr am unteren Rand fixiert, sondern rutscht nach oben oder überlappt den Content.

## Analyse
- Wahrscheinlich wurden durch neue Features (z. B. Drag & Drop, Video-Player-Integration) CSS-Regeln oder Container-Strukturen verändert, die das Tab-Layout und die Footer-Positionierung beeinflussen.
- Mögliche Ursachen:
  - Flexbox/Grid-Container fehlen oder sind falsch verschachtelt.
  - Footer hat kein `position: fixed`/`sticky` oder der Parent-Container hat keine volle Höhe (`min-height: 100vh`).
  - Neue Styles überschreiben bestehende Layout-Regeln.

## ToDo / Fix-Vorschlag
- CSS/HTML der Tab-Container und des Footers prüfen und anpassen:
  - Flexibles Layout für Tabs sicherstellen.
  - Footer mit `position: fixed` oder `sticky` und `bottom: 0` verankern.
  - Parent-Container auf volle Höhe setzen.
- Regressionstest nach jeder UI-Änderung durchführen.

## Ergebnis (offen)
- Nach CSS/HTML-Korrektur sollten Tabs und Footer wieder wie gewohnt funktionieren.
