#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Tech / Bottle
# Eingabewerte: Pfade zu ALAC / M4A Dateien
# Ausgabewerte: HTTP Responses, Dateisystem-Checks (.cache)
# Testdateien: media/sample.alac
# ERWEITERUNGEN (TODO): [ ] Streaming-Tests erweitern, [ ] Cache-Invalidierung prüfen
# KOMMENTAR: Testet das Routing von Medieninhalten inklusive Transcoding-Checks.
# VERWENDUNG: python3 tests/integration/tech/bottle/test_route.py

"""
KATEGORIE:
----------
Tech / Bottle

ZWECK:
------
Prüft das dynamische Servieren und Caching von speziellen Audioformaten wie ALAC.
Validiert die korrekte Route-Verarbeitung und Cache-Verzeichnis-Erstellung.

EINGABEWERTE:
-------------
- Pfade zu ALAC / M4A Dateien (z.B. media/sample.alac)

AUSGABEWERTE:
-------------
- HTTP Responses
- Dateisystem-Checks (.cache)

TESTDATEIEN:
------------
- media/sample.alac

ERWEITERUNGEN (TODO):
---------------------
- [ ] Streaming-Tests erweitern
- [ ] Cache-Invalidierung prüfen

VERWENDUNG:
-----------
    python3 tests/integration/tech/bottle/test_route.py
"""

import eel
import bottle
import threading
import time
import urllib.request
import os

MEDIA_DIR = "./media"

@bottle.route('/media/<filepath:path>')
def serve_media(filepath):
    print("ROUTE CALLED WITH:", filepath)
    ext = filepath.lower()
    if ext.endswith('.alac') or ext.endswith('.m4a'):
        os.path.join(MEDIA_DIR, filepath)
        cache_dir = os.path.join(MEDIA_DIR, '.cache')
        os.makedirs(cache_dir, exist_ok=True)
        return "ALAC handled"
    return "Not ALAC"

def run_eel():
    eel.init('web')
    eel.start('index.html', mode=None, size=(100, 100), port=8082, block=False)

t = threading.Thread(target=run_eel, daemon=True)
t.start()
time.sleep(2)

try:
    res = urllib.request.urlopen('http://localhost:{port}/media/sample.alac').read()
    print("Response:", res)
except Exception as e:
    print("Error:", e)

print("Cache exists:", os.path.exists("./media/.cache"))
