import pytest
import subprocess
from pathlib import Path
import sys
import os
import importlib
from unittest.mock import patch

def get_project_root():
    return Path(__file__).parent.parent

def test_version_consistency():
    """Verify that version strings are consistent across the project."""
    root = get_project_root()
    version_file = root / "VERSION"
    assert version_file.exists(), "VERSION file missing"
    version = version_file.read_text().strip()
    
    # Check main.py
    sys.path.insert(0, str(root))
    with patch('env_handler.validate_safe_startup'), patch('eel.init'), patch('eel.expose'):
        import main
        importlib.reload(main)
        assert main.VERSION == version, f"main.py version ({main.VERSION}) != VERSION file ({version})"
    
    # Check debian control
    control_file = root / "packaging" / "DEBIAN" / "control"
    if control_file.exists():
        with open(control_file, 'r') as f:
            content = f.read()
            import re
            match = re.search(r'^Version:\s*(.*)$', content, re.MULTILINE)
            if match:
                assert match.group(1).strip() == version, f"Control file version ({match.group(1).strip()}) != VERSION file ({version})"

def test_run_all_tests():
    """Run all tests in the tests/ directory and ensure they pass."""
    root = get_project_root()
    # Skip this test folder itself to avoid recursion or just run pytest on the whole dir
    # We use subprocess to run pytest as a standalone process
    result = subprocess.run(
        ["pytest", "tests/test_environment_dependencies.py", "tests/test_environment_isolation.py", "tests/test_media_item_logic.py"],
        cwd=root,
        capture_output=True,
        text=True
    )
    print(result.stdout)
    assert result.returncode == 0 or "FAILED" not in result.stdout, f"Some tests failed:\n{result.stdout}"

def test_build_deb_script():
    """Verify that the build_deb.sh script exists and is executable."""
    root = get_project_root()
    build_script = root / "build_deb.sh"
    assert build_script.exists(), "build_deb.sh missing"
    assert os.access(build_script, os.X_OK), "build_deb.sh is not executable"

if __name__ == "__main__":
    import os
    pytest.main([__file__])
