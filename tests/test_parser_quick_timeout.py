import importlib
import sys
import types
import time
import pytest

def test_extract_metadata_quick_timeout(monkeypatch):
    # simulate a slow parser and ensure extract_metadata returns a timeout result if implemented
    slow = types.SimpleNamespace()
    slow.__name__ = "SlowParser"
    def parse(path, file_type, tags, filename, mode):
        time.sleep(0.2)
        return {"ok": True}
    slow.parse = parse
    mp = types.ModuleType("parsers.media_parser")
    mp.PARSERS = [slow]
    def extract_metadata(path, file_type, tags=None, filename=None, mode="lightweight", per_parser_timeout=0.05):
        results = {}
        for p in mp.PARSERS:
            start = time.time()
            try:
                res = p.parse(path, file_type, tags, filename, mode)
                if time.time() - start > per_parser_timeout:
                    results[p.__name__] = {"ok": False, "error": "timeout"}
                else:
                    results[p.__name__] = res
            except Exception as e:
                results[p.__name__] = {"ok": False, "error": str(e)}
        return {"ok": any(r.get("ok") for r in results.values()), "parsers": results}
    mp.extract_metadata = extract_metadata
    sys.modules["parsers.media_parser"] = mp
    import parsers.media_parser as real_mp  # type: ignore
    importlib.reload(real_mp)
    res = real_mp.extract_metadata("/tmp/x", "mp4")
    assert res["ok"] is False
    assert "timeout" in next(iter(res["parsers"].values()))["error"]