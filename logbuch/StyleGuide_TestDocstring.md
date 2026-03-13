# Style Guide: Test-Docstrings & Vorlage playx_media

## Ziel
Die Docstrings in Testskripten sollen klar, prägnant und ohne doppelte Informationen gestaltet werden. Die Funktion playx_media dient als Vorlage für strukturierte, aber nicht redundante Docstrings.

---

## Vorlage: playx_media
```python
def playx_media(media_path, options=None):
    """
    Startet die Wiedergabe einer Mediendatei.
    
    Args:
        media_path (str): Pfad zur Mediendatei.
        options (dict, optional): Zusätzliche Wiedergabeoptionen.
    
    Returns:
        bool: True bei Erfolg, False bei Fehler.
    """
    pass
```

---

## Style Guide für Test-Docstrings
- Keine doppelte Information: Header und Docstring sollen sich nicht wiederholen.
- Docstring enthält nur Zweck, Parameter und Rückgabewert.
- Zusätzliche Testdaten, Eingabewerte, Ausgabewerte und TODOs werden im Skript-Header dokumentiert, nicht im Docstring.
- Docstrings nach PEP 257 und Google/Numpy-Style.

### Beispiel für Testfunktion
```python
def test_db_initialization():
    """
    Prüft, ob die Datenbank korrekt initialisiert und alle Tabellen angelegt werden.
    """
    # ...Testcode...
```

---

## Vorteile
- Klare Trennung zwischen Skript-Header (Meta-Info) und Docstring (Funktionsbeschreibung).
- Weniger Redundanz, bessere Lesbarkeit.
- IDE- und Doku-Tools können gezielt Informationen extrahieren.

---

**Letzte Aktualisierung:** 13. März 2026
