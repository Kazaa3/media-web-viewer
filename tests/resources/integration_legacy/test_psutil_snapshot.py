# =============================================================================
# Kategorie: PSUtil Snapshot Test
# Eingabewerte: PSUtil-Kommandos, Testdaten
# Ausgabewerte: Speicher- und CPU-Ausgaben
# Testdateien: test_psutil_snapshot.py
# Kommentar: Testet die PSUtil-Snapshot-Funktionalität.
# =============================================================================
"""
PSUtil Snapshot Test Suite (DE/EN)
==================================

DE:
Testet die Snapshot-Funktionalität von PSUtil für Speicher und CPU.

EN:
Tests PSUtil snapshot functionality for memory and CPU.

Autor/Author: Media Web Viewer Team
Erstellt/Created: 2026-03-13
Version: 1.0.0
"""

import pytest

def test_psutil_snapshot_presence():
    """
    DE:
    Testet, ob PSUtil installiert ist und Snapshots für Speicher und CPU erstellt werden können.

    EN:
    Tests if PSUtil is installed and snapshots for memory and CPU can be created.
    Returns:
        Keine.
    Raises:
        pytest.skip: Wenn PSUtil nicht installiert.
        AssertionError: Wenn Snapshots nicht erstellt werden können.
    """
    try:
        import psutil
    except ImportError:
        pytest.skip("psutil not installed")
    mem = psutil.virtual_memory()
    assert hasattr(mem, "total")
    assert psutil.cpu_percent(interval=0.1) is not None