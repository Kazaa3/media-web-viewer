# Kategorie: Eel / Bottle Integration
# Eingabewerte: Pfade zu Mediendateien
# Ausgabewerte: Statische Dateien über HTTP
# Testdateien: Keine (Benötigt lokales /media Verzeichnis)
# Kommentar: Prüft ob Bottle-Routen innerhalb der Eel-Umgebung korrekt registriert und aufgelöst werden.

import eel
import bottle
import time
import urllib.request
import threading
import os

import tempfile
import shutil

def test_static_route_registration():
    """Checks if static routes can be registered without opening a browser."""
    
    # Use a temporary directory for the media root to avoid permission issues in /opt
    with tempfile.TemporaryDirectory() as tmp_media:
        test_file = os.path.join(tmp_media, "test_eel.txt")
        with open(test_file, "w") as f:
            f.write("eel_static_test_content")

        @bottle.route('/media-test/<filepath:path>')
        def serve_media(filepath):
            return bottle.static_file(filepath, root=tmp_media)

        # Start headless on a different port to avoid conflicts
        t = threading.Thread(target=lambda: eel.start('app.html', mode=None, block=True, port=8889), daemon=True)
        t.start()
        
        time.sleep(1.5)

        try:
            response = urllib.request.urlopen('http://localhost:8889/media-test/test_eel.txt', timeout=5).read().decode('utf-8')
            assert response == "eel_static_test_content"
        finally:
            pass # tempfile cleans up

if __name__ == "__main__":
    eel.init('web')
    test_static_route_registration()
    print("Test passed!")
