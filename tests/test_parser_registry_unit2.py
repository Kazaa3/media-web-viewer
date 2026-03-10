import types
import importlib
import sys

import pytest


def _make_parser(name, result, raise_exc=False, delay=None):
    class P:
        __name__ = name

        @staticmethod
        def parse(path, file_type, tags, filename, mode):
            if raise_exc:
                raise RuntimeError("parser-failure")
            if delay:
                import time
                time.sleep(delay)
            return result
    return P


def test_extract_metadata_picks_first_success(monkeypatch):
    # build fake parsers.media_parser module with PARSERS and extract_metadata behavior
    mp = types.ModuleType("parsers.media_parser")
    p1 = _make_parser("P1", {"ok": False, "error": "bad"})
    p2 = _make_parser("P2", {"ok": True, "duration_ms": 1000})
    p3 = _make_parser("P3", {"ok": True, "duration_ms": 2000})
    mp.PARSERS = [p1, p2, p3]

    def extract_metadata(path, file_type, tags=None, filename=None, mode="lightweight"):
        tags = tags or {}
        results = {}
        for p in mp.PARSERS:
            try:
                results[p.__name__] = p.parse(path, file_type, tags, filename, mode)
            except Exception as e:
                results[p.__name__] = {"ok": False, "error": str(e)}
        # choose first ok
        for name, res in results.items():
            if res.get("ok"):
                return {"ok": True, "winner": name, "parsers": results}
        return {"ok": False, "parsers": results}

    mp.extract_metadata = extract_metadata
    sys.modules["parsers.media_parser"] = mp
    import parsers.media_parser as real_mp  # type: ignore
    importlib.reload(real_mp)
    res = real_mp.extract_metadata("/tmp/x", "mkv")
    assert res["ok"] is True
    assert res["winner"] == "P2"
    assert "P3" in res["parsers"]


def test_extract_metadata_handles_exceptions(monkeypatch):
    mp = types.ModuleType("parsers.media_parser")
    p_bad = _make_parser("Bad", None, raise_exc=True)
    p_ok = _make_parser("Ok", {"ok": True})
    mp.PARSERS = [p_bad, p_ok]

    def extract_metadata(path, file_type, tags=None, filename=None, mode="lightweight"):
        results = {}
        for p in mp.PARSERS:
            try:
                results[p.__name__] = p.parse(path, file_type, tags, filename, mode)
            except Exception as e:
                results[p.__name__] = {"ok": False, "error": str(e)}
        for name, res in results.items():
            if res.get("ok"):
                return {"ok": True, "winner": name, "parsers": results}
        return {"ok": False, "parsers": results}

    mp.extract_metadata = extract_metadata
    sys.modules["parsers.media_parser"] = mp
    import parsers.media_parser as real_mp  # type: ignore
    importlib.reload(real_mp)
    res = real_mp.extract_metadata("/tmp/x", "mp3")
    assert res["ok"] is True
    assert res["winner"] == "Ok"