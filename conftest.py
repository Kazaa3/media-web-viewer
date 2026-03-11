import sys
import os

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
