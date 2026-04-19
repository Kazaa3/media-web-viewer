import pytest
import os
import sys
from pathlib import Path

# Add project root to sys.path
from src.core.config_master import PROJECT_ROOT, DB_FILENAME, TEST_DIR, DATA_DIR
if str(PROJECT_ROOT) not in sys.path:

def test_debug_db_stats_label():
    """Checks if the debug tab labels match the user requirement 'database item'."""
    app_html_path = PROJECT_ROOT / "web" / "app.html"
    assert app_html_path.exists()
    
    with open(app_html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # User specifically wanted "database item: 0" (or similar)
    # My implementation added "database item:" as a bold label.
    assert "database item:" in content.lower(), "Label 'database item:' not found in app.html"

def test_debug_tab_json_logic():
    """Checks for presence of JSON display logic in the debug tab."""
    app_html_path = PROJECT_ROOT / "web" / "app.html"
    with open(app_html_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Check for the element ID
    assert 'id="debug-items-json"' in content
    
    # Check for the logic that populates it with system environment
    assert 'JSON.stringify(debugConsole.env' in content or 'JSON.stringify(debugConsole.debug_flags' in content

if __name__ == "__main__":
    try:
        test_debug_db_stats_label()
        print("✅ Debug DB Label Test: OK")
        test_debug_tab_json_logic()
        print("✅ Debug Tab JSON Logic: OK")
    except AssertionError as e:
        print(f"❌ Test failed: {e}")
        exit(1)
