# Test Header Style Guide (All Variants)

## Standard Header (DE/EN)

```python
# =============================================================================
# Kategorie: <Test-Kategorie>
# Eingabewerte: <Inputs>
# Ausgabewerte: <Outputs>
# Testdateien: <Testdateien>
# Kommentar: <Kommentar>
# Startbefehl: <Befehl>
# =============================================================================
"""
<Test Suite Title> (DE/EN)
=========================

DE:
<Deutsche Beschreibung>

EN:
<English Description>

Autor/Author: <Name>
Erstellt/Created: <Datum>
Version: <Version>
Lizenz: <Lizenz>
"""
```

## Minimal Header Variant

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: <Test-Kategorie>
# Eingabewerte: <Inputs>
# Ausgabewerte: <Outputs>
# Testdateien: <Testdateien>
# Kommentar: <Kommentar>
"""
<Test Suite Title>

<Description>

<License>
"""
```

## Extended Header Variant (with License)

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: <Test-Kategorie>
# Eingabewerte: <Inputs>
# Ausgabewerte: <Outputs>
# Testdateien: <Testdateien>
# Kommentar: <Kommentar>
"""
<Test Suite Title> (DE/EN)
=========================

DE:
<Deutsche Beschreibung>

EN:
<English Description>

Autor/Author: <Name>
Erstellt/Created: <Datum>
Version: <Version>
Lizenz: GPLv3
"""
```

## Docstring Style (Google/Bilingual)

- Use Google-style docstrings for all functions/classes.
- Provide both German and English descriptions.
- Example:

```python
class ExampleTest(unittest.TestCase):
    """
    DE:
    Testet die Beispiel-Funktion.

    EN:
    Tests the example function.
    """
    def test_example(self):
        """
        DE:
        Prüft, ob Beispiel korrekt funktioniert.

        EN:
        Verifies correct example behavior.
        Returns:
            Keine.
        Raises:
            AssertionError: Wenn Fehler.
        """
        pass
```

---

> Document all header variants in this file. Reference this guide for test file headers and docstring conventions.
