import sys
import os
import shutil
import pytest
from pathlib import Path

# Ensure project root is first on sys.path so local modules are imported
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Remove any packaging-installed copies that might shadow local modules
PACKAGING_MARKER = os.path.join('packaging', 'opt', 'media-web-viewer')
removed = []
for p in list(sys.path):
    if PACKAGING_MARKER in p.replace('\\', '/'):
        sys.path.remove(p)
        removed.append(p)

# Also purge any modules already loaded from the packaging path
for name, mod in list(sys.modules.items()):
    try:
        f = getattr(mod, '__file__', None)
        if f and PACKAGING_MARKER in f.replace('\\', '/'):
            del sys.modules[name]
    except Exception:
        pass


def pytest_collection_modifyitems(config, items):
    """Skip tests that require external binaries or testdata not present in this environment.

    This keeps the test run focused on unit-level logic and avoids failures
    caused by missing sample files or system binaries during local runs.
    """
    testdata_dir = Path(__file__).parent / "testdata"
    has_testdata = testdata_dir.exists()

    def should_skip(item):
        name = str(item.fspath)
        nid = item.nodeid
        # Format coverage requires testdata files
        if name.endswith('tests/test_format_coverage.py') and not has_testdata:
            return "missing testdata folder"
        # ffprobe tests require ffprobe or pymediainfo; skip if neither available
        if 'test_ffprobe' in nid:
            if shutil.which('ffprobe') is None and 'pymediainfo' not in sys.modules and importlib.util.find_spec('pymediainfo') is None:
                return "missing ffprobe/pymediainfo"
        # network tests expect a running local server
        if name.endswith('tests/test_network.py'):
            return "network tests skipped in local runs"
        return None

    import importlib
    for item in list(items):
        reason = should_skip(item)
        if reason:
            item.add_marker(pytest.mark.skip(reason=reason))
