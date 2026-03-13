# =============================================================================
# Kategorie: Mutagen Compatibility Helper
# Eingabewerte: MP4 Kapitel-Start, Titel
# Ausgabewerte: Shim-Objekt mit start und title
# Testdateien: _mutagen_compat.py
# Kommentar: Kompatibilitäts-Helfer für Mutagen Kapitel-Tests.
# =============================================================================
"""
Mutagen Compatibility Helper (DE/EN)
=====================================

DE:
Hilft bei der Kompatibilität von MP4 Kapitel-Objekten für Tests.

EN:
Helper for MP4 chapter object compatibility in tests.
Simple compatibility helper used by tests to represent MP4 chapters.

Avoid constructing real `mutagen.mp4.MP4Chapters` objects because different
mutagen versions expose different constructors and may attempt file/atom
parsing during construction which breaks test collection. Instead return a
lightweight object with `start` and `title` attributes.

Autor/Author: Media Web Viewer Team
Erstellt/Created: 2026-03-13
Version: 1.0.0
"""

class _Shim:
    """
    DE:
    Einfaches Shim-Objekt für Kapitel mit start und title.

    EN:
    Simple shim object for chapters with start and title.
    """
    def __init__(self, start, title):
        self.start = start
        self.title = title

def MP4Chapters(start=None, title=None, **kwargs):
    """
    DE:
    Erstellt ein Shim-Kapitelobjekt für Tests.

    EN:
    Creates a shim chapter object for tests.
    Returns:
        _Shim: Kapitelobjekt mit start und title.
    """
    return _Shim(start, title)
