# =============================================================================
# Kategorie: Subprocess Safety Test
# Eingabewerte: Dateipfad, ffprobe_parser
# Ausgabewerte: Argument-Listen, Fehlerbehandlung
# Testdateien: test_subprocess_safety.py
# Kommentar: Testet sichere Argumentübergabe und subprocess.run ohne shell=True.
# Startbefehl: pytest tests/test_subprocess_safety.py -v
# =============================================================================
"""
Subprocess Safety Test Suite (DE/EN)
====================================

DE:
Testet die sichere Übergabe von Argumenten an subprocess.run und stellt sicher, dass keine Shell-Injektion möglich ist.

EN:
Tests safe argument passing to subprocess.run and ensures no shell injection is possible.

Autor/Author: Media Web Viewer Team
Erstellt/Created: 2026-03-13
Version: 1.0.0
"""

import subprocess
import importlib
import pytest

def test_ffprobe_parser_uses_list_args_and_no_shell(monkeypatch):
    """
    DE:
    Testet, ob ffprobe_parser subprocess.run mit einer Argumentliste und ohne shell=True aufruft.

    EN:
    Tests if ffprobe_parser calls subprocess.run with a list of arguments and without shell=True.

    Args:
        monkeypatch: pytest fixture zum Patchen von Funktionen.
    Returns:
        Keine.
    Raises:
        AssertionError: Wenn subprocess.run nicht korrekt verwendet wird.
    """
    try:
        from src.parsers import ffprobe_parser as fp  # type: ignore
    except Exception:
        pytest.skip("ffprobe_parser not present")
    called = {}

    def fake_run(*args, **kwargs):
        called["args"] = args
        called["kwargs"] = kwargs
        class P:
            returncode = 0
            stdout = "{}"
            stderr = ""
        return P()
    monkeypatch.setattr(subprocess, "run", fake_run)
    fp.parse("/tmp/weird;rm -rf /", None, None, None, mode="lightweight")
    assert "args" in called
    # first positional arg should be the command list
    cmd = called["args"][0]
    assert isinstance(cmd, list), "subprocess.run called with a non-list command"
    # ensure not using shell=True
    assert called["kwargs"].get("shell", False) is False