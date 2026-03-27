import pytest
import time

def test_psutil_metrics_snapshot():
    try:
        import psutil
    except ImportError:
        pytest.skip("psutil not installed")
    # quick snapshot
    cpu = psutil.cpu_percent(interval=0.01)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/") if hasattr(psutil, "disk_usage") else None
    assert isinstance(cpu, float)
    assert hasattr(mem, "total")
    if disk is not None:
        assert hasattr(disk, "total")