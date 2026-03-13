import time
import pytest

def test_get_server_status_repeated_calls():
    try:
        import src.core.main as m  # type: ignore
    except Exception:
        pytest.skip("main not importable")
    # warmup
    _ = m.get_server_status()
    # repeated calls should not raise and should be reasonably fast
    start = time.time()
    for _ in range(100):
        st = m.get_server_status()
        assert isinstance(st, dict)
    duration = time.time() - start
    assert duration < 5.0  # smoke threshold