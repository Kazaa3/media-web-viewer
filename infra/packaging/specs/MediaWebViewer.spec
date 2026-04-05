# -*- mode: python ; coding: utf-8 -*-
import sys
import os
from pathlib import Path

# Dynamic project root resolution
# In PyInstaller spec files, __file__ is not defined, but SPECPATH is available.
SPEC_DIR = Path(SPECPATH).resolve()
PROJECT_ROOT = SPEC_DIR.parent.parent.parent

VERSION = '1.34'

# Dynamic path resolution
eel_path = None
try:
    import eel
    eel_path = os.path.dirname(eel.__file__)
except ImportError:
    pass

datas = [(str(PROJECT_ROOT / 'web'), 'web')]
if eel_path:
    datas.append((os.path.join(eel_path, 'eel.js'), 'eel'))

a = Analysis(
    [str(PROJECT_ROOT / 'src' / 'core' / 'main.py')],
    pathex=[str(PROJECT_ROOT)],
    binaries=[],
    datas=datas,
    hiddenimports=['bottle_websocket', 'gevent', 'gevent.monkey'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name=f'MediaWebViewer-{VERSION}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
