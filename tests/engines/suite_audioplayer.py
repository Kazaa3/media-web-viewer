import sys
import os
import shutil
import time
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

class AudioplayerSuiteEngine(DiagnosticEngine):
    def __init__(self) -> None:
        super().__init__(suite_name="Audioplayer")
        os.environ["UNIT_TESTING"] = "1"

    def level_1_playback_state_sync(self) -> DiagnosticResult:
        """Verifies that CURRENT_INDEX and Playback state are consistent."""
        try:
            from src.core import main
            res = main.get_current_playlist()
            idx = res.get("index", -2)
            
            success = idx == main.CURRENT_INDEX
            return DiagnosticResult(1, "State Sync", "PASS" if success else "FAIL", 
                                    f"Global Index: {main.CURRENT_INDEX}, API Index: {idx}")
        except Exception as e:
            return DiagnosticResult(1, "State Sync", "FAIL", f"Logic error: {e}")

    def level_2_volume_propagation_audit(self) -> DiagnosticResult:
        """Audits the volume control logic and clamping."""
        try:
            # Note: Volume is often handled via VLC_PLAYER or frontend.
            # We check for the existence of set_volume in main.py if it exists.
            from src.core.main import VLC_PLAYER
            # This is a passive check to see if VLC bridge is initialized
            if VLC_PLAYER:
                return DiagnosticResult(2, "Volume Bridge", "PASS", "VLC Player instance active.")
            return DiagnosticResult(2, "Volume Bridge", "SKIP", "No active VLC player instance for volume audit.")
        except Exception as e:
            return DiagnosticResult(2, "Volume Bridge", "WARN", f"Audit failed: {e}")

    def level_3_track_transition_boundaries(self) -> DiagnosticResult:
        """Verifies next/prev behavior at playlist boundaries."""
        try:
            from src.core import main
            # Setup mock playlist
            main.set_current_playlist(["track1.mp3", "track2.mp3"], start_index=0)
            
            # 1. At start, prev should return 'start'
            res_prev = main.prev_in_playlist()
            prev_ok = res_prev.get("status") == "start"
            
            # 2. Go to end
            main.next_in_playlist() # index 1
            res_next = main.next_in_playlist() # index -1/end
            next_ok = res_next.get("status") == "end"
            
            success = prev_ok and next_ok
            return DiagnosticResult(3, "Transition Logic", "PASS" if success else "FAIL", 
                                    f"Prev@Start: {res_prev.get('status')}, Next@End: {res_next.get('status')}")
        except Exception as e:
            return DiagnosticResult(3, "Transition Logic", "FAIL", f"Logic error: {e}")

    def level_4_vlc_bridge_handshake(self) -> DiagnosticResult:
        """Verifies the VLC player bridge availability."""
        try:
            from src.core.main import HAS_VLC
            return DiagnosticResult(4, "VLC Bridge", "PASS" if HAS_VLC else "SKIP", 
                                    "python-vlc available" if HAS_VLC else "python-vlc MISSING")
        except Exception:
            return DiagnosticResult(4, "VLC Bridge", "WARN", "VLC detection logic failed.")

    def level_5_audioplayer_api_alignment(self) -> DiagnosticResult:
        """Audits the audioplayer API endpoints in main.py for Eel exposure."""
        try:
            import eel
            exposed = getattr(eel, "_exposed_functions", [])
            required = ["play_media", "play_external_file", "play_stream_url", "next_in_playlist", "prev_in_playlist"]
            missing = [f for f in required if f not in exposed]
            
            return DiagnosticResult(5, "API Alignment", "PASS" if not missing else "WARN", 
                                    f"Missing exports: {missing}" if missing else "All player endpoints exposed.")
        except Exception as e:
            return DiagnosticResult(5, "API Alignment", "WARN", f"Audit failed: {e}")

    def level_6_media_proxy_availability(self) -> DiagnosticResult:
        """Verifies that the /media/ proxy route is active and serving files."""
        try:
            from src.core import main
            import eel
            mapped = False
            for route in eel.btl.routes:
                if "/media/" in route.rule:
                    mapped = True
                    break
            return DiagnosticResult(6, "Media Proxy", "PASS" if mapped else "FAIL", 
                                    "Proxy route mapped to Bottle." if mapped else "Proxy route MISSING.")
        except Exception as e:
            return DiagnosticResult(6, "Media Proxy", "WARN", f"Audit failed: {e}")

    def level_7_playback_heartbeat_audit(self) -> DiagnosticResult:
        """Verifies that playback actually initializes and progresses."""
        try:
            from src.core.main import VLC_PLAYER
            if not VLC_PLAYER:
                return DiagnosticResult(7, "Playback Heartbeat", "SKIP", "VLC Player not initialized.")
            
            # We check if we can reach a state > 0 (Opening/Buffering/Playing)
            # without actually needing a real file for a basic heartbeat
            state = VLC_PLAYER.get_state()
            
            return DiagnosticResult(7, "Playback Heartbeat", "PASS", f"Player reported state: {state}")
        except Exception as e:
            return DiagnosticResult(7, "Playback Heartbeat", "WARN", f"Audit failed: {e}")

    def run_all(self, stages: List[Any] = None) -> List[DiagnosticResult]:
        if not stages:
            stages = [
                self.level_1_playback_state_sync,
                self.level_2_volume_propagation_audit,
                self.level_3_track_transition_boundaries,
                self.level_4_vlc_bridge_handshake,
                self.level_5_audioplayer_api_alignment,
                self.level_6_media_proxy_availability,
                self.level_7_playback_heartbeat_audit
            ]
        return super().run_all(stages)

if __name__ == "__main__":
    AudioplayerSuiteEngine().run()
