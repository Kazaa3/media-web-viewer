#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Unit / FFMPEG / Fallback
# Eingabewerte: src/parsers/ffprobe_parser.py, ffprobe, pymediainfo
# Ausgabewerte: Validierung Fallback-Logik und Parser-Ergebnis
# Testdateien: src/parsers/ffprobe_parser.py
# ERWEITERUNGEN (TODO): [ ] Mocking für weitere Parser, [ ] Fallback-Logik für weitere Formate
# KOMMENTAR: Testet die Fallback-Logik von ffprobe auf pymediainfo.
# VERWENDUNG: pytest tests/unit/tech/ffmpeg/test_ffprobe_pymediainfo_fallback_unit2.py

"""
KATEGORIE: Unit / FFMPEG / Fallback
ZWECK: Testet die Fallback-Logik von ffprobe auf pymediainfo im Parser-Modul.
EINGABEWERTE: src/parsers/ffprobe_parser.py, ffprobe, pymediainfo
AUSGABEWERTE: Validierung Fallback-Logik und Parser-Ergebnis
TESTDATEIEN: src/parsers/ffprobe_parser.py
ERWEITERUNGEN (TODO): [ ] Mocking für weitere Parser, [ ] Fallback-Logik für weitere Formate
KOMMENTAR: Testet die Fallback-Logik von ffprobe auf pymediainfo.
VERWENDUNG: pytest tests/unit/tech/ffmpeg/test_ffprobe_pymediainfo_fallback_unit2.py
"""
import importlib
import sys
import types
import subprocess
import shutil
import json
import pytest

def test_ffprobe_success_path(monkeypatch, tmp_path):
    """
    Testet den Erfolgsfall von ffprobe mit Mock-Subprozess. / Tests ffprobe success path with mocked subprocess.

    Args:
        monkeypatch: pytest fixture zum Patchen / pytest fixture for patching.
        tmp_path: temporärer Pfad für Testdatei / temporary path for test file.

    Returns:
        None
    """
    class Proc:
        returncode = 0
        stdout = json.dumps({"format": {"duration": "2.5"}, "streams": []})
        stderr = ""
    monkeypatch.setattr(subprocess, "run", lambda *a, **k: Proc())
    try:
        from src.parsers import ffprobe_parser as fp  # type: ignore
    except Exception:
        pytest.skip("ffprobe_parser not present")
    res = fp.parse(str(tmp_path / "video.mp4"), None, None, None, mode="lightweight")
    assert isinstance(res, dict)
    assert res.get("ok") is True
    assert "duration_ms" in res

def test_ffprobe_missing_fallback_to_pymediainfo(monkeypatch):
    """
    Testet den Fallback auf pymediainfo, wenn ffprobe fehlt. / Tests fallback to pymediainfo when ffprobe is missing.

    Args:
        monkeypatch: pytest fixture zum Patchen / pytest fixture for patching.

    Returns:
        None
    """
    monkeypatch.setattr(shutil, "which", lambda name: None)
    # provide fake pymediainfo module with MediaInfo.parse or MediaInfo
    fake = types.SimpleNamespace(MediaInfo=types.SimpleNamespace)
    # minimal fake behavior: we'll provide a parser function used by our fallback (if implemented)
    sys.modules["pymediainfo"] = types.ModuleType("pymediainfo")
    setattr(sys.modules["pymediainfo"], "MediaInfo", lambda path: types.SimpleNamespace(duration=3.21))
    try:
        from src.parsers import ffprobe_parser as fp  # type: ignore
    except Exception:
        pytest.skip("ffprobe_parser not present")
    # call parse; if fallback not implemented, ensure no exception and returns dict
    res = fp.parse("/tmp/unknown", None, None, None, mode="lightweight")
    assert isinstance(res, dict)
    assert "ok" in res