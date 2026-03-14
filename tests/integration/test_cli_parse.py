# =============================================================================
# Kategorie: CLI Parse Test
# Eingabewerte: CLI-Argumente, Dateipfad, Output-Option
# Ausgabewerte: Metadata-Extraktion, JSON-Ausgabe
# Testdateien: test_cli_parse.py
# Kommentar: Testet mwv-cli parse Kommando und Metadata-Extraktion.
# Startbefehl: pytest tests/test_cli_parse.py -v
# =============================================================================
"""
CLI Parse Test Suite (DE/EN)
============================

DE:
Testet das mwv-cli parse Kommando und die Metadata-Extraktion.

EN:
Tests the mwv-cli parse command and metadata extraction.

Autor/Author: Media Web Viewer Team
Erstellt/Created: 2026-03-13
Version: 1.0.0
"""

import os
import pytest

# Unit test placeholder for mwv-cli parse command.
# Skips if `cli` module is not yet implemented; when implemented this test
# verifies that `cli.main(['parse', path, '--output', out])` calls
# `extract_metadata()` with the given path and writes JSON output.

cli = pytest.importorskip("cli", reason="mwv-cli not implemented yet")

def test_cli_parse_calls_extract_metadata(monkeypatch, tmp_path):
    """
    DE:
    Testet, ob extract_metadata korrekt aufgerufen und JSON ausgegeben wird.

    EN:
    Tests if extract_metadata is called correctly and JSON is output.
    Args:
        monkeypatch: pytest fixture zum Patchen.
        tmp_path: pytest fixture für temporäre Dateien.
    Returns:
        Keine.
    Raises:
        AssertionError: Wenn Pfad oder Output nicht korrekt.
    """
    called = {}

    def fake_extract_metadata(path, *args, **kwargs):
        called['path'] = path
        return {'mock': 'metadata'}

    monkeypatch.setattr(cli, 'extract_metadata', fake_extract_metadata)

    out_file = tmp_path / "meta.json"
    argv = ['parse', '/some/media/file.mp3', '--output', str(out_file)]

    # assume cli.main accepts argv list
    cli.main(argv)

    assert called.get('path') == '/some/media/file.mp3'
    assert out_file.exists()
    content = out_file.read_text()
    assert 'mock' in content
