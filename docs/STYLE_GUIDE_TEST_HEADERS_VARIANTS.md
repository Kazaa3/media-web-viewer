# Test Header Variants Reference

This document lists all header variants used in Media Web Viewer test files.

## Variant 1: Standard Project Header

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

## Variant 2: Minimal Header

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

## Variant 3: Extended Header (with License)

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

---

> Use this reference for all test file header variants. See also STYLE_GUIDE_TEST_HEADERS.md for docstring conventions.
