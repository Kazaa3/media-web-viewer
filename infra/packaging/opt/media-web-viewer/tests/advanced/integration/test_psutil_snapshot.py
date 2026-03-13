import pytest

def test_psutil_snapshot_presence():
    try:
        import psutil
    except ImportError:
        pytest.skip("psutil not installed")
    mem = psutil.virtual_memory()
    assert hasattr(mem, "total")
    assert psutil.cpu_percent(interval=0.1) is not None