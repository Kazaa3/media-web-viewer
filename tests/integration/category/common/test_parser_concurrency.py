import importlib
import sys
import types
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import pytest

def _make_slow_parser(name, sleep_s=0.05):
    p = types.SimpleNamespace()
    p.__name__ = name

    def parse(path, file_type, tags, filename, mode):
        time.sleep(sleep_s)
        return {"ok": True, "duration_ms": 100}
    p.parse = parse
    return p

def test_extract_metadata_concurrent(monkeypatch):
    # Build fake parsers.media_parser with multiple slow parsers
    mp = types.ModuleType("src.parsers.media_parser")
    mp.PARSERS = [_make_slow_parser("P1", 0.05), _make_slow_parser("P2", 0.02)]

    def extract_metadata(path, file_type, tags=None, filename=None, mode="lightweight"):
        results = {}
        for p in mp.PARSERS:
            try:
                results[p.__name__] = p.parse(path, file_type, tags, filename, mode)
            except Exception as e:
                results[p.__name__] = {"ok": False, "error": str(e)}
        return {"ok": any(r.get("ok") for r in results.values()), "parsers": results}

    mp.extract_metadata = extract_metadata
    sys.modules["src.parsers.media_parser"] = mp
    import parsers.media_parser as real_mp  # type: ignore
    importlib.reload(real_mp)

    # run multiple concurrent extract_metadata calls and assert all succeed
    with ThreadPoolExecutor(max_workers=4) as ex:
        futures = [ex.submit(real_mp.extract_metadata, f"/tmp/{i}.mp4", "mp4") for i in range(8)]
        for fut in as_completed(futures, timeout=5):
            res = fut.result()
            assert res["ok"] is True
            assert "parsers" in res