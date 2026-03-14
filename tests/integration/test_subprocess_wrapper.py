# =============================================================================
# Kategorie: Subprocess Wrapper Test
# Eingabewerte: Dateipfade, ffprobe-Kommandos
# Ausgabewerte: Argument-Listen, Fehlerbehandlung
# Testdateien: test_subprocess_wrapper.py
# Kommentar: Testet die sichere Argumentübergabe an ffprobe Wrapper.
# =============================================================================
"""
Subprocess Wrapper Test Suite (DE/EN)
=====================================

DE:
Testet die sichere Übergabe von Argumenten an den ffprobe Wrapper, insbesondere für Dateinamen mit Leerzeichen und Sonderzeichen.

EN:
Tests safe argument passing to the ffprobe wrapper, especially for filenames with spaces and special characters.

Autor/Author: Media Web Viewer Team
Erstellt/Created: 2026-03-13
Version: 1.0.0
"""

import os
import pytest
import subprocess

# Placeholder test for safe subprocess wrapper (ffprobe fallback)
# Skips if the expected module `tools.ffprobe_wrapper` is not present.

ffw = pytest.importorskip("tools.ffprobe_wrapper", reason="ffprobe wrapper not implemented")

def test_ffprobe_wrapper_uses_list_args(monkeypatch):
    """
    DE:
    Testet, ob der ffprobe Wrapper Argumente als Liste übergibt und Dateinamen korrekt verarbeitet.
    EN:
    Tests if the ffprobe wrapper passes arguments as a list and processes filenames correctly.
    """
    captured = {}

    def fake_run(args, stdout, stderr, check):
        captured['args'] = args
        class Dummy:
            stdout = b'{}'
        return Dummy()

    monkeypatch.setattr(subprocess, 'run', fake_run)

    # call wrapper with a filename that might contain spaces and special chars
    ffw.run_ffprobe('/media/smb/test file (1).mp3')

    assert isinstance(captured.get('args'), list)
    assert '/media/smb/test file (1).mp3' in captured['args']
