# Kategorie: Routing Test
# Eingabewerte: Pfade zu ALAC / M4A Dateien
# Ausgabewerte: HTTP Responses, Dateisystem-Checks (.cache)
# Testdateien: media/sample.alac
# Kommentar: Prüft das dynamische Servieren und Caching von speziellen Audioformaten wie ALAC.

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
    res = urllib.request.urlopen('http://localhost:8080/media/sample.alac').read()
    print("Response:", res)
except Exception as e:
    print("Error:", e)

print("Cache exists:", os.path.exists("./media/.cache"))
