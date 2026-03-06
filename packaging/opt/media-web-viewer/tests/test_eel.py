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

def test_static_route_registration():
    """Checks if static routes can be registered without opening a browser."""
    
    # Use a dummy media file for testing
    os.makedirs("./media", exist_ok=True)
    with open("./media/test_eel.txt", "w") as f:
        f.write("eel_static_test_content")

    @bottle.route('/media/<filepath:path>')
    def serve_media(filepath):
        return bottle.static_file(filepath, root='./media')

    # Start headless on a different port to avoid conflicts
    t = threading.Thread(target=lambda: eel.start('app.html', mode=None, block=True, port=8889), daemon=True)
    t.start()
    
    time.sleep(1.5)

    try:
        response = urllib.request.urlopen('http://localhost:8889/media/test_eel.txt', timeout=5).read().decode('utf-8')
        assert response == "eel_static_test_content"
    finally:
        if os.path.exists("./media/test_eel.txt"):
            os.remove("./media/test_eel.txt")

if __name__ == "__main__":
    eel.init('web')
    test_static_route_registration()
    print("Test passed!")
