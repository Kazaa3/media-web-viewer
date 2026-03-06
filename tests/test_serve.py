# Kategorie: Server Test (Eel/Bottle)
# Eingabewerte: HTTP Requests an localhost
# Ausgabewerte: HTTP Responses ("Hello")
# Testdateien: Keine
# Kommentar: Prüft ob die Eel/Bottle Server-Integration korrekt auf Anfragen reagiert.

import eel
import bottle
import time
import urllib.request
import threading

def test_server_startup():
    """Starts Eel with a headless mode (no browser) to test routing."""
    
    @bottle.route('/testroute')
    def test_route():
        return "Hello"

    # Start Eel in a separate thread because it's blocking
    # We use 'none' as mode to prevent ANY browser window from opening
    t = threading.Thread(target=lambda: eel.start('index.html', mode=None, block=True, port=8888), daemon=True)
    t.start()
    
    # Give the server a moment to start
    time.sleep(1.5)

    try:
        response = urllib.request.urlopen('http://localhost:8888/testroute', timeout=5).read().decode('utf-8')
        assert response == "Hello", f"Expected 'Hello', got '{response}'"
    finally:
        # We don't have a clean way to stop the Eel thread here without exiting path,
        # but as it's a daemon thread in a subprocess (if run via main process), it's fine for a unit test.
        pass

if __name__ == "__main__":
    # If run directly
    eel.init('web')
    test_server_startup()
    print("Test passed!")
