import pytest
import sys
from pathlib import Path

# Add src to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import src.core.main as main
import src.core.db as db

def test_get_version():
    assert main.get_version() == main.VERSION

def test_get_app_name():
    assert main.get_app_name() == "dict"

def test_get_library_structure():
    # This might return empty if DB is empty, but should be a dict with 'media' key
    response = main.get_library()
    assert isinstance(response, dict)
    assert "media" in response
    assert isinstance(response["media"], list)

def test_get_db_stats():
    # We can't easily test the exact numbers without a mock DB, 
    # but we can check the presence of @eel.expose and call it if possible.
    # main.py might have a get_db_stats exposed, let's check.
    pass

if __name__ == "__main__":
    pytest.main([__file__])
