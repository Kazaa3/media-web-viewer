import eel
import bottle
from main import MEDIA_DIR

@bottle.route('/media/<filepath:path>')
def serve_media(filepath):
    return bottle.static_file(filepath, root=MEDIA_DIR)

eel.init("web")
# start server in thread so we can test it
import threading
server_thread = threading.Thread(target=eel.start, args=("index.html",), kwargs={"size": (1000, 600), "block": False})
server_thread.daemon = True
server_thread.start()

import time
import urllib.request
time.sleep(2) # wait for server to start

try:
    url = "http://localhost:8000/media/sample.flac"
    response = urllib.request.urlopen(url)
    print("SUCCESS: Got status code", response.getcode())
except Exception as e:
    print("FAILED:", e)

