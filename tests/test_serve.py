import eel
import bottle

@bottle.route('/testroute')
def test():
    return "Hello"

eel.init('web')
# eel.start uses a blocking call. We can start it with block=False
eel.start('index.html', size=(100, 100), block=False)

import time
time.sleep(1)

import urllib.request
try:
    print(urllib.request.urlopen('http://localhost:8000/testroute').read().decode('utf-8'))
except Exception as e:
    print(e)
    try:
        # Eel's default port might not be 8000. It's usually 8000.
        pass
    except: pass
