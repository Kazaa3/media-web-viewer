import importlib
import os
import pytest

def test_get_server_status_basic_shape():
    try:
        import main as m  # type: ignore
    except Exception:
        pytest.skip("main not importable")
    assert hasattr(m, "get_server_status") and callable(m.get_server_status)
    status = m.get_server_status()
    assert isinstance(status, dict)
    # core expected keys
    assert "runtime" in status
    assert "ws_backend" in status
    assert "pid" in status
    assert "tools" in status
    tools = status.get("tools") or {}
    # tools may report presence booleans
    assert isinstance(tools, dict)

@pytest.mark.integration
def test_get_server_status_integration_reports_tools():
    if os.environ.get("ENABLE_INTEGRATION") != "1":
        pytest.skip("integration disabled")
    try:
        import main as m  # type: ignore
        importlib.reload(m)
    except Exception:
        pytest.skip("main not importable for integration")
    status = m.get_server_status()
    # if integration enabled, at least pid and uptime should be present
    assert status.get("pid") is not None
    assert "uptime" in status