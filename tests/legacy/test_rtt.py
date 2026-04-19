import pytest
import time
import json
import sys
from pathlib import Path

# Add src to sys.path
from src.core.config_master import PROJECT_ROOT, DB_FILENAME, TEST_DIR, DATA_DIR

from src.core.main import rtt_ping, confirm_receipt, sanitize_json_utf8

def test_sanitize_json_utf8():
    data = {
        "valid": "hello",
        "invalid": b"\xff".decode('latin-1'),
        "nested": {"list": ["a", "b", 123]}
    }
    sanitized = sanitize_json_utf8(data)
    assert sanitized["valid"] == "hello"
    assert isinstance(sanitized["invalid"], str)
    assert sanitized["nested"]["list"][2] == 123

def test_rtt_ping_structure():
    test_data = {
        "stage1": {"a": 1},
        "stage2": {"nested": {"b": 2}},
        "stage3": [{"id": 1}]
    }
    response = rtt_ping(test_data)
    assert response["status"] == "pong"
    assert "timestamp" in response
    assert response["echo"] == test_data

def test_confirm_receipt():
    response = confirm_receipt("TEST_EVENT")
    assert response["status"] == "log_noted"

if __name__ == "__main__":
    pytest.main([__file__])
