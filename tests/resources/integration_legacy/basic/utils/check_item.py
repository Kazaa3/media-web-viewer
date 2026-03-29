#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: MediaItem Creation Test
# Eingabewerte: media/*.mp*, media/*.mkv, media/*.we*
# Ausgabewerte: MediaItem.tags Dictionary für alle gefundenen Dateien
# Testdateien: Alle media/*.mp*, *.mkv, *.we* Dateien
# Kommentar: Erstellt MediaItem für alle gefundenen Media-Dateien und dumpt Tags (diagnostischer Test für Parser-Integration).
import glob
import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
    sys.path.insert(0, os.path.join(PROJECT_ROOT, "src"))

from src.core.main import MediaItem

for d in ['/usr/lib/python3/dist-packages', '/usr/local/lib/python3.10/dist-packages']:
    sys.path.append(os.path.join(d, 'site-packages'))

media_dir = os.path.join(PROJECT_ROOT, "media")
files = (
    glob.glob(os.path.join(media_dir, "*.mp*"))
    + glob.glob(os.path.join(media_dir, "*.mkv"))
    + glob.glob(os.path.join(media_dir, "*.we*"))
)
for f in files:
    try:
        item = MediaItem(f, f)
        print(f"File: {f}")
        print(f"Tags: {item.tags}")
        print("-" * 50)
    except Exception as e:
        print(f"Failed on {f}: {e}")
