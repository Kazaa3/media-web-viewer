# Kategorie: Netzwerk & Integration Test
# Kommentar: Konsolidierte Tests mit dynamischem Port und vereinfachtem Routing.

import eel
import time
import urllib.request
import threading
import os
import tempfile
import socket
import shutil

def get_free_port():
    """Findet einen freien Port auf dem System."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port

# Wir nutzen einen Port, der sicher frei ist
TEST_PORT = get_free_port()
TMP_DIR = tempfile.mkdtemp()

def setup_module():
    eel.init('web')

    # Vereinfachte Routen ohne komplexe Platzhalter zum Testen
    @eel.btl.route('/ping')
    def ping():
        return "pong"

    @eel.btl.route('/echo-test')
    def echo():
        # Testet ob Query-Parameter funktionieren (Alternative zu Pfad-Parametern)
        name = eel.btl.request.query.get('name', 'unknown')
        return f"hello {name}"

    @eel.btl.route('/static-direct')
    def static_direct():
        # Absoluter Pfad-Test ohne Platzhalter
        return eel.btl.static_file("test.txt", root=TMP_DIR)

    # Server starten
    t = threading.Thread(
        target=lambda: eel.start('app.html', mode=None, block=True, port=TEST_PORT),
        daemon=True
    )
    t.start()
    time.sleep(3.0)

def teardown_module():
    if os.path.exists(TMP_DIR):
        shutil.rmtree(TMP_DIR)

def test_ping():
    url = f"http://localhost:{TEST_PORT}/ping"
    res = urllib.request.urlopen(url, timeout=5).read().decode('utf-8')
    assert res == "pong"

def test_echo_query():
    # Test über Query-String statt Pfad-Parameter
    url = f"http://localhost:{TEST_PORT}/echo-test?name=world"
    res = urllib.request.urlopen(url, timeout=5).read().decode('utf-8')
    assert res == "hello world"

def test_static_file_fixed():
    # Wir erstellen die Datei im TMP_DIR
    with open(os.path.join(TMP_DIR, "test.txt"), "w") as f:
        f.write("fix_content")

    url = f"http://localhost:{TEST_PORT}/static-direct"
    res = urllib.request.urlopen(url, timeout=5).read().decode('utf-8')
    assert res == "fix_content"

if __name__ == "__main__":
    setup_module()
    try:
        test_ping()
        test_echo_query()
        test_static_file_fixed()
        print("✅ test_network.py passed")
    finally:
        teardown_module()
