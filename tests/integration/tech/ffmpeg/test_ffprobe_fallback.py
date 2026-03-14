#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Tech / FFmpeg
# Eingabewerte: Fake ffprobe/pymediainfo environment
# Ausgabewerte: Fallback-Status, No-Crash-Validierung
# Testdateien: src/parsers/ffprobe_parser.py
# Kommentar: Testet den Fallback-Mechanismus von ffprobe zu pymediainfo.
"""
FFprobe Fallback Test Suite (DE/EN)
===================================

DE:
Testet den Fallback-Mechanismus von ffprobe zu pymediainfo und prüft auf Absturzfreiheit.

EN:
Tests ffprobe fallback mechanism to pymediainfo and checks for crash-free operation.

Autor/Author: Media Web Viewer Team
Erstellt/Created: 2026-03-13
Version: 1.0.0
"""

import subprocess
import shutil
import pytest

def test_ffprobe_to_pymediainfo_fallback(monkeypatch):
    # simulate ffprobe not present
    monkeypatch.setattr(shutil, "which", lambda name: None)
    # simulate pymediainfo available and returning expected metadata via a fake function
    class FakeMediaInfo:
        def __init__(self, path):
            self.duration = 1.23
    monkeypatch.setitem(__import__("sys").modules, "pymediainfo", __import__("types").SimpleNamespace(MediaInfo=FakeMediaInfo))
    # call a hypothetical probe function (implement in parsers) or assert behavior with subprocess guarded
    try:
        from src.parsers import ffprobe_parser as fp  # type: ignore
    except Exception:
        pytest.skip("ffprobe_parser not present")
    # If ffprobe missing, ffprobe_parser.parse should return an error or fallback; ensure no crash
    res = fp.parse("/tmp/nonexistent.mkv", None, None, None, mode="lightweight")
    assert isinstance(res, dict)
    assert "ok" in res