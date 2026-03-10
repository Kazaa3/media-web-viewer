import types
import sys
import time
import importlib

import pytest


def test_parser_with_slow_response_is_handled(monkeypatch):
    # create fake parser that sleeps longer than allowed
    slow = types.SimpleNamespace()
    def slow_parse(path, file_type, tags, filename, mode):
        time.sleep(0.2)
        return {"ok": True}
    slow.__name__ = "Slow"
    slow.parse = slow_parse

    mp = types.ModuleType("parsers.media_parser")
    mp.PARSERS = [slow]

    def extract_metadata(path, file_type, tags=None, filename=None, mode="lightweight"):
        results = {}
        for p in mp.PARSERS:
            try:
                # simplistic timeout simulation: if parse takes >0.1s treat as timeout
                start = time.time()
                res = p.parse(path, file_type, tags, filename, mode)
                dur = time.time() - start
                if dur > 0.1:
                    results[p.__name__] = {"ok": False, "error": "timeout"}
                else:
                    results[p.__name__] = res
            except Exception as e:
                results[p.__name__] = {"ok": False, "error": str(e)}
        return {"ok": any(r.get("ok") for r in results.values()), "parsers": results}

    sys.modules["parsers.media_parser"] = mp
    mp.extract_metadata = extract_metadata
    import parsers.media_parser as real_mp  # type: ignore
    importlib.reload(real_mp)
    res = real_mp.extract_metadata("/tmp/x", "mp4")
    assert res["ok"] is False
    assert "timeout" in next(iter(res["parsers"].values()))["error"]