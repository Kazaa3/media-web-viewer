# Kategorie: Direct Path Routing Test
# Eingabewerte: Pfad "media/..."
# Ausgabewerte: HTTP Response von der Route
# Testdateien: 02 We the People….m4a
# Kommentar: Testet ob die Route auch bei vorangestelltem "media/" im Pfad korrekt greift.

import eel
import bottle
import threading
import time
import urllib.request
import urllib.parse

MEDIA_DIR = "./media"

@bottle.route('/media/<filepath:path>')
def serve_media(filepath):
    print("SERVE_MEDIA CALLED WITH:", filepath)
    return "SUCCESS_BOTTLE"

# Eel setup
eel.init('web')

def run_eel():
    # Use block=False and a different port
    eel.start('index.html', mode=None, size=(100, 100), port=8083, block=False)
    while True:
        time.sleep(1)

t = threading.Thread(target=run_eel, daemon=True)
t.start()
time.sleep(2)

try:
    filename = urllib.parse.quote("media/02 We the People….m4a")
    print("Requesting:", f'http://localhost:8083/{filename}')
    res = urllib.request.urlopen(f'http://localhost:8083/{filename}').read()
    print("Response:", res)
except Exception as e:
    print("Error:", e)
