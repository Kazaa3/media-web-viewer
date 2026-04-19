import sys
import os
import shutil
import time
import subprocess
from pathlib import Path
from typing import List, Dict, Any

from src.core.config_master import PROJECT_ROOT, DB_FILENAME, TEST_DIR, DATA_DIR
sys.path.append(str(PROJECT_ROOT))
sys.path.append(str(PROJECT_ROOT / "src"))

# Diagnostic Base
try:
    from tests.engines.test_base import DiagnosticEngine, DiagnosticResult
except ImportError:
    from test_base import DiagnosticEngine, DiagnosticResult

class CastingSuiteEngine(DiagnosticEngine):
    def __init__(self) -> None:
        super().__init__(suite_name="Casting")
        os.environ["UNIT_TESTING"] = "1"

    def level_1_binary_audit(self) -> DiagnosticResult:
        """Audits the availability of librespot and swyh-rs binaries."""
        librespot = shutil.which("librespot")
        swyh = shutil.which("swyh-rs")
        
        details = []
        if librespot: details.append(f"librespot: {librespot}")
        else: details.append("librespot: MISSING")
        
        if swyh: details.append(f"swyh-rs: {swyh}")
        else: details.append("swyh-rs: MISSING")
        
        success = librespot is not None or swyh is not None
        return DiagnosticResult(1, "Binary Audit", "PASS" if success else "WARN", 
                                " | ".join(details))

    def level_2_pychromecast_readiness(self) -> DiagnosticResult:
        """Verifies if pychromecast and zeroconf are installed and importable."""
        try:
            import pychromecast
            import zeroconf
            return DiagnosticResult(2, "PyChromecast Ready", "PASS", 
                                    f"pychromecast v{pychromecast.__version__}")
        except ImportError as e:
            return DiagnosticResult(2, "PyChromecast Ready", "FAIL", f"Missing dependency: {e}")

    def level_3_chromecast_discovery_smoke(self) -> DiagnosticResult:
        """Performs a non-blocking mDNS discovery smoke test for Chromecasts."""
        try:
            import pychromecast
            # Non-blocking discovery with short timeout
            browser = pychromecast.get_chromecasts(timeout=2)
            # browser is (list of services, browser_obj)
            devices = browser[0] if isinstance(browser, tuple) else []
            
            return DiagnosticResult(3, "Discovery Smoke", "PASS" if devices else "SKIP", 
                                    f"Found {len(devices)} devices in 2s.")
        except Exception as e:
            return DiagnosticResult(3, "Discovery Smoke", "WARN", f"Discovery failed: {e}")

    def level_4_spotify_bridge_dry_run(self) -> DiagnosticResult:
        """Verifies the Spotify bridge (librespot) invocation logic."""
        # We don't want to start a real long-running process, just check logic
        try:
            from src.core import main
            res = main.start_spotify_bridge()
            success = res.get("status") == "ok"
            return DiagnosticResult(4, "Spotify Bridge", "PASS" if success else "FAIL", 
                                    res.get("details", "No details"))
        except Exception as e:
            return DiagnosticResult(4, "Spotify Bridge", "FAIL", f"Logic error: {e}")

    def level_5_swyh_rs_toggle_logic(self) -> DiagnosticResult:
        """Verifies the swyh-rs toggle logic state transitions."""
        try:
            from src.core import main
            res_on = main.toggle_swyh_rs(enabled=True)
            res_off = main.toggle_swyh_rs(enabled=False)
            
            success = res_on.get("state") == "enabled" and res_off.get("state") == "disabled"
            return DiagnosticResult(5, "swyh-rs Toggle", "PASS" if success else "FAIL", 
                                    f"Transitions: {res_on.get('state')} -> {res_off.get('state')}")
        except Exception as e:
            return DiagnosticResult(5, "swyh-rs Toggle", "FAIL", f"Logic error: {e}")

    def level_6_casting_api_alignment(self) -> DiagnosticResult:
        """Audits the casting API endpoints in main.py for Eel exposure."""
        try:
            import eel
            exposed = getattr(eel, "_exposed_functions", [])
            required = ["discover_cast_devices", "start_cast", "toggle_swyh_rs", "start_spotify_bridge"]
            missing = [f for f in required if f not in exposed]
            
            return DiagnosticResult(6, "API Alignment", "PASS" if not missing else "WARN", 
                                    f"Missing exports: {missing}" if missing else "All casting endpoints exposed.")
        except Exception as e:
            return DiagnosticResult(6, "API Alignment", "WARN", f"Audit failed: {e}")

    def run_all(self, stages: List[Any] = None) -> List[DiagnosticResult]:
        if not stages:
            stages = [
                self.level_1_binary_audit,
                self.level_2_pychromecast_readiness,
                self.level_3_chromecast_discovery_smoke,
                self.level_4_spotify_bridge_dry_run,
                self.level_5_swyh_rs_toggle_logic,
                self.level_6_casting_api_alignment
            ]
        return super().run_all(stages)

if __name__ == "__main__":
    CastingSuiteEngine().run()
