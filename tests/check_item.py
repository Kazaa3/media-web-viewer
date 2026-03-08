#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: MediaItem Creation Test
# Eingabewerte: media/*.mp*, media/*.mkv, media/*.we*
# Ausgabewerte: MediaItem.tags Dictionary für alle gefundenen Dateien
# Testdateien: Alle media/*.mp*, *.mkv, *.we* Dateien
# Kommentar: Erstellt MediaItem für alle gefundenen Media-Dateien und dumpt Tags (diagnostischer Test für Parser-Integration).
import glob
from main import MediaItem
import sys
import os

for d in ['/usr/lib/python3/dist-packages', '/usr/local/lib/python3.10/dist-packages']:
    sys.path.append(os.path.join(d, 'site-packages'))

files = glob.glob("media/*.mp*") + glob.glob("media/*.mkv") + glob.glob("media/*.we*")
for f in files:
    try:
        item = MediaItem(f, f)
        print(f"File: {f}")
        print(f"Tags: {item.tags}")
        print("-" * 50)
    except Exception as e:
        print(f"Failed on {f}: {e}")
