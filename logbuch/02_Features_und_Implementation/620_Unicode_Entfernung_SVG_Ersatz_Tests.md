# Logbuch: Unicode-Entfernung & SVG-Ersatz in Tests

**Datum:** 16. März 2026

## Änderung: Unicode entfernt, SVG ersetzt

- In allen relevanten Testdateien wurden Unicode-Symbole entfernt und durch SVG-Icons ersetzt.
- Ziel: Maximale Kompatibilität und Stabilität der Testausführung, insbesondere bei Headless- und CI-Umgebungen.
- Betroffene Bereiche: Player-Controls, UI-Buttons, Statusanzeigen in Test- und UI-Komponenten.
- Alle Tests wurden nach der Umstellung erfolgreich mit `pytest tests` ausgeführt.

---

**Ergebnis:**
- Keine Unicode-Fehler mehr in Testausgaben oder UI.
- SVG-Icons sorgen für konsistente Darstellung und bessere Wartbarkeit.

Weitere Details siehe vorherige Logbuch-Einträge und Testskripte.
