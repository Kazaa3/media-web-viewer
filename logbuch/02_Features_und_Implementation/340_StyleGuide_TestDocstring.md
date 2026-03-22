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

## Docstring-Definition nach playx_media (Deutsch/Englisch, Google-Standard, Light-Variante)

### Vorlage (Deutsch/Englisch, Google-Style, Light)
```python
def playx_media(media_path, options=None):
    """
    Startet die Wiedergabe einer Mediendatei. / Starts playback of a media file.

    Args:
        media_path (str): Pfad zur Mediendatei / Path to media file.
        options (dict, optional): Zusätzliche Wiedergabeoptionen / Additional playback options.

    Returns:
        bool: True bei Erfolg, False bei Fehler / True if successful, False otherwise.
    """
    pass
```

---

## Google-Style (Basic) Docstring – Doppelsprache für Refactoring

### Vorlage (Deutsch/Englisch, Google-Style, Basic)
```python
def playx_media(media_path, options=None):
    """
    Startet die Wiedergabe einer Mediendatei. / Starts playback of a media file.

    Args:
        media_path (str): Pfad zur Mediendatei / Path to media file.
        options (dict, optional): Zusätzliche Wiedergabeoptionen / Additional playback options.

    Returns:
        bool: True bei Erfolg, False bei Fehler / True if successful, False otherwise.
    """
    pass
```

---

## Anweisung für Refactoring
- Docstrings müssen beim Refactoring in Deutsch und Englisch (doppelsprache) nach Google-Style (basic) verfasst werden.
- Die Vorlage oben ist verbindlich für alle Test- und Projektfunktionen.
- Keine Meta-Informationen oder redundante Kommentare im Docstring.

---

**Letzte Aktualisierung:** 13. März 2026
