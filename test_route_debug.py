import eel
import bottle
import threading
import time
import urllib.request
import os

MEDIA_DIR = "./media"

@bottle.route('/media/<filepath:path>')
def serve_media(filepath):
    print("SERVE_MEDIA CALLED WITH:", filepath)
    return "SUCCESS_BOTTLE"

# Eel setup
eel.init('web')

def run_eel():
    eel.start('index.html', size=(100, 100), port=8082, block=False)
    while True:
        time.sleep(1)

t = threading.Thread(target=run_eel, daemon=True)
t.start()
time.sleep(2)

try:
    # URL encode the filename just in case
    import urllib.parse
    filename = urllib.parse.quote("02 We the People….m4a")
    res = urllib.request.urlopen(f'http://localhost:8082/media/{filename}').read()
    print("Response:", res)
except Exception as e:
    print("Error:", e)
