#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Pyscreeze Requirements Test
# Eingabewerte: Pyscreeze library
# Ausgabewerte: API-Prüfung
# Testdateien: Keine
# Kommentar: Prüft Pyscreeze-API-Präsenz.
"""
Pyscreeze Requirements Test Suite (DE/EN)
=========================================

DE:
Testet die API-Präsenz von Pyscreeze.

EN:
Tests API presence of Pyscreeze.

Autor/Author: Media Web Viewer Team
Erstellt/Created: 2026-03-13
Version: 1.0.0
"""

import pytest

def test_pyscreeze_import_and_api():
    """
    DE:
    Prüft, ob Pyscreeze importierbar ist und API-Funktionen vorhanden sind.

    EN:
    Verifies Pyscreeze is importable and API functions are present.
    Returns:
        Keine.
    Raises:
        pytest.skip: Wenn Pyscreeze nicht installiert.
        AssertionError: Wenn API-Funktionen fehlen.
    """
    try:
        import pyscreeze
    except Exception:
        pytest.skip("pyscreeze not installed")
    # basic API sanity checks (do not perform real screenshot in unit gate)
    assert hasattr(pyscreeze, "screenshot")
    assert hasattr(pyscreeze, "locateOnScreen") or hasattr(pyscreeze, "locate")