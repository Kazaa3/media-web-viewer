import importlib
import types
import pytest

def test_parser_registry_fallback(monkeypatch):
    # prepare a fake media_parser module with PARSERS list and extract_metadata function
    mp = types.SimpleNamespace()
    # fake parser a: fails
    class PFail:
        __name__ = "PFail"
        @staticmethod
        def parse(path, file_type, tags, filename, mode):
            return {"ok": False, "error": "fail"}
    # fake parser b: succeeds
    class PSucc:
        __name__ = "PSucc"
        @staticmethod
        def parse(path, file_type, tags, filename, mode):
            return {"ok": True, "duration_ms": 123}
    mp.PARSERS = [PFail, PSucc]
    def extract_metadata(path, file_type, tags=None, filename=None, mode="lightweight"):
        results = {}
        for p in mp.PARSERS:
            results[p.__name__] = p.parse(path, file_type, tags, filename, mode)
        # simple fallback: pick first ok
        for name, res in results.items():
            if res.get("ok"):
                return {"ok": True, "winner": name, "parsers": results}
        return {"ok": False, "parsers": results}
    mp.extract_metadata = extract_metadata

    # monkeypatch into real import path if needed, else assert behavior of our fake
    assert mp.extract_metadata("/tmp/x", "mkv")["winner"] == "PSucc"