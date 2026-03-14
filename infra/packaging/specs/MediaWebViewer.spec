# -*- mode: python ; coding: utf-8 -*-
import sys
import os
from pathlib import Path

VERSION = '1.34'

# Dynamic path resolution
eel_path = None
try:
    import eel
    eel_path = os.path.dirname(eel.__file__)
except ImportError:
    pass

datas = [('web', 'web')]
if eel_path:
    datas.append((os.path.join(eel_path, 'eel.js'), 'eel'))

a = Analysis(
    ['main.py'],
    pathex=[],
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
    name='MediaWebViewer',
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
