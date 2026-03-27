import sys
import os
import time
import urllib.request
import threading
import socket
import tempfile
import shutil
from pathlib import Path
from typing import List, Dict, Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))
sys.path.append(str(PROJECT_ROOT / "src"))

# Diagnostic Base
try:
    from tests.engines.test_base import DiagnosticEngine, DiagnosticResult
except ImportError:
    from test_base import DiagnosticEngine, DiagnosticResult

def get_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port

class NetworkIntegrationSuiteEngine(DiagnosticEngine):
    def __init__(self) -> None:
        super().__init__(suite_name="Network")
        self.test_port = get_free_port()
        self.tmp_dir = Path(tempfile.mkdtemp())
        os.environ["UNIT_TESTING"] = "1"

    def level_1_server_ping(self) -> DiagnosticResult:
        """Verifies that the Eel/Bottle server responds to a ping (Legacy: test_network.py)."""
        import eel
        eel.init(str(PROJECT_ROOT / "web"))
        
        @eel.btl.route('/ping')
        def ping(): return "pong"
        
        # Start server in thread
        t = threading.Thread(
            target=lambda: eel.start('app.html', mode=None, block=True, port=self.test_port),
            daemon=True
        )
        t.start()
        time.sleep(2.0) # Wait for startup
        
        try:
            url = f"http://localhost:{self.test_port}/ping"
            res = urllib.request.urlopen(url, timeout=3).read().decode('utf-8')
            success = res == "pong"
            return DiagnosticResult(1, "Server Ping", "PASS" if success else "FAIL", f"Received: {res}")
        except Exception as e:
            return DiagnosticResult(1, "Server Ping", "FAIL", f"Connection failed: {e}")

    def level_2_static_file_serving(self) -> DiagnosticResult:
        """Verifies that the server can serve static files from a temp directory."""
        import eel
        test_file = self.tmp_dir / "diag_static.txt"
        test_file.write_text("live_content")
        
        @eel.btl.route('/diag-static')
        def diag_static():
            return eel.btl.static_file(test_file.name, root=str(self.tmp_dir))
            
        try:
            url = f"http://localhost:{self.test_port}/diag-static"
            res = urllib.request.urlopen(url, timeout=3).read().decode('utf-8')
            success = res == "live_content"
            return DiagnosticResult(2, "Static Serving", "PASS" if success else "FAIL", f"Served content: {res}")
        except Exception as e:
            return DiagnosticResult(2, "Static Serving", "FAIL", f"Failed: {e}")

    def run_all(self, stages: List[Any] = None) -> List[DiagnosticResult]:
        if not stages:
            stages = [self.level_1_server_ping, self.level_2_static_file_serving]
        results = super().run_all(stages)
        # Cleanup
        if self.tmp_dir.exists():
            shutil.rmtree(self.tmp_dir)
        return results

if __name__ == "__main__":
    NetworkIntegrationSuiteEngine().run_all()
