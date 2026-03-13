# Parser-Pipeline Härten: Fehlerrobustheit und Performance

## Ziel
Die Parser-Pipeline wird so gestaltet, dass sie robust gegenüber Fehlern und Ausreißern ist. Typische Fehler werden früh abgefangen, die Pipeline kann bei kritischen Problemen kurzschließen und die Performance bleibt messbar.

## Maßnahmen
- Early Exit: Nicht verarbeitbare Dateien werden sofort übersprungen.
- Fehler-Shortcircuit: Typische Parser-Fehler werden abgefangen und führen nicht zum Abbruch der gesamten Pipeline.
- Logging: Fehler und Ausreißer werden protokolliert und für spätere Analyse gespeichert.
- Performance-Messung: Zeit pro Parser und Datei wird erfasst (z.B. mit time.time()).
- Test-Suite: Spezialfälle und Fehler werden gezielt getestet.

## Beispiel: Fehlerbehandlung im Python-Code
```python
def extract_metadata(path, file_type, tags, filename, mode):
    try:
        # Parser-Kette
        for parser in parser_list:
            result = parser.parse(path, file_type, tags, filename, mode)
            if result is not None:
                return result
    except (IOError, ValueError) as e:
        logger.error(f"Parser-Fehler: {e}")
        return None
```

## Hinweis: Hörbücher sind kein eigener Item-Typ auf der GUI
- Hörbücher werden in der Parser-Pipeline und im Backend wie andere Medien behandelt.
- In der GUI gibt es keinen separaten Typ oder Tab für Hörbücher.
- Die Darstellung erfolgt über die allgemeinen Medienlisten (Audio, Musik, etc.).
- Filter und Sortierung können genutzt werden, um Hörbücher gezielt anzuzeigen.
- Spezialbehandlung (z.B. Cover, Kapitel) erfolgt ggf. über Metadaten, aber nicht als eigener Typ.

---
Letzte Aktualisierung: 11. März 2026