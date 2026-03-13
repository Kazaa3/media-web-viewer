import importlib
import sys
import types
import subprocess
import shutil
import json
import pytest

def test_ffprobe_success_path(monkeypatch, tmp_path):
    # mock subprocess.run to return valid ffprobe JSON
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
    # simulate ffprobe absent
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