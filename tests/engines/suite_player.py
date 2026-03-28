import sys
import os
import json
import subprocess
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

class MockProcess:
    def __init__(self, cmd=None):
        self.cmd = cmd
        self.returncode = 0
        self.terminated = False
        self.pid = 9999
        self.stdout = type('stdout', (), {'__iter__': lambda s: iter(["Encoding: 100.0 %"]), 'close': lambda s: None})()
    def terminate(self): self.terminated = True
    def wait(self, timeout=None): pass
    def poll(self): return 0
    def kill(self): self.terminated = True

class PlayerSuiteEngine(DiagnosticEngine):
    def __init__(self) -> None:
        super().__init__(suite_name="Player")
        os.environ["UNIT_TESTING"] = "1"

    def level_1_seeking_injection(self) -> DiagnosticResult:
        """Verifies that the -ss flag is correctly injected into FFmpeg commands."""
        from src.core.streams import hls_stream as hls
        from src.core.streams import mse_stream as mse
        import subprocess
        import os
        
        captured_cmds = []
        original_popen = subprocess.Popen
        original_exists = os.path.exists
        
        def mock_popen(cmd, *args, **kwargs):
            captured_cmds.append(cmd)
            return MockProcess(cmd)
            
        subprocess.Popen = mock_popen
        os.path.exists = lambda x: True # Mock all files as existing
        
        try:
            hls.start_hls_fmp4("/t.mkv", "/tmp/hls", "test_hls", start_time=120)
            mse.start_mse_stream("/t.mkv", "test_mse", start_time=60)
            
            hls_ok = any(isinstance(cmd, list) and "-ss" in cmd and "120.0" in cmd for cmd in captured_cmds)
            mse_ok = any(isinstance(cmd, list) and "-ss" in cmd and "60" in cmd for cmd in captured_cmds)
            
            success = hls_ok and mse_ok
            return DiagnosticResult(1, "Seeking Injection", "PASS" if success else "FAIL", 
                                    f"HLS SS Injection: {hls_ok}, MSE SS Injection: {mse_ok}")
        finally:
            subprocess.Popen = original_popen
            os.path.exists = original_exists

    def level_2_session_lifecycle(self) -> DiagnosticResult:
        """Verifies that starting a new stream stops the previous one."""
        from src.core.streams import mse_stream as mse
        import subprocess
        import os
        
        processes = []
        original_popen = subprocess.Popen
        original_exists = os.path.exists
        
        def mock_popen(*args, **kwargs):
            p = MockProcess()
            processes.append(p)
            return p
            
        subprocess.Popen = mock_popen
        os.path.exists = lambda x: True
        
        try:
            mse.start_mse_stream("/t.mkv", "sid_1")
            if not processes:
                return DiagnosticResult(2, "Session Lifecycle", "FAIL", "No process started for first session.")
            
            p1 = processes[0]
            mse.start_mse_stream("/t.mkv", "sid_1")
            
            success = p1.terminated
            return DiagnosticResult(2, "Session Lifecycle", "PASS" if success else "FAIL", "Previous process terminated on restart.")
        finally:
            subprocess.Popen = original_popen
            os.path.exists = original_exists

    def level_3_hw_acceleration(self) -> DiagnosticResult:
        """Verifies player streams respect hardware encoder detection."""
        from src.core.streams import hls_stream as hls
        from src.core import hardware_detector
        import subprocess
        
        original_hw = hardware_detector.get_best_hw_encoder
        hardware_detector.get_best_hw_encoder = lambda: "nvenc_h264"
        
        captured_cmds = []
        original_popen = subprocess.Popen
        def mock_popen(cmd, *args, **kwargs):
            captured_cmds.append(cmd)
            return MockProcess(cmd)
        subprocess.Popen = mock_popen

        try:
            hls.start_hls_fmp4("/t.mkv", "/tmp/hls", "hw_test")
            success = any("nvenc_h264" in cmd for cmd in captured_cmds)
            return DiagnosticResult(3, "HW Acceleration", "PASS" if success else "FAIL", "nvenc_h264 found in encoder mapping.")
        finally:
            hardware_detector.get_best_hw_encoder = original_hw
            subprocess.Popen = original_popen

    def level_4_vlc_bridge_logic(self) -> DiagnosticResult:
        """Verifies VLC bridge command generation."""
        from src.core.streams import vlc_bridge
        import subprocess
        
        original_popen = subprocess.Popen
        captured_cmds = []
        def mock_popen(cmd, *args, **kwargs):
            captured_cmds.append(cmd)
            return MockProcess(cmd)
        subprocess.Popen = mock_popen
        
        try:
            vlc_bridge.start_vlc_bridge("/t.mkv", port=8080)
            success = any("vlc" in str(cmd[0]).lower() and "--sout" in cmd for cmd in captured_cmds)
            return DiagnosticResult(4, "VLC Bridge Logic", "PASS" if success else "FAIL", "VLC sout transcode command generated.")
        finally:
            subprocess.Popen = original_popen

    def level_5_seeking_precision(self) -> DiagnosticResult:
        """Verifies float-based seeking precision for ffmpeg."""
        from src.core.streams import hls_stream as hls
        import subprocess
        
        captured_cmds = []
        original_popen = subprocess.Popen
        def mock_popen(cmd, *args, **kwargs):
            captured_cmds.append(cmd)
            return MockProcess(cmd)
        subprocess.Popen = mock_popen

        try:
            hls.start_hls_fmp4("/t.mkv", "/tmp/hls", "math_test", start_time=3661.55)
            # Should be "-ss", "3661.55"
            success = any("-ss" in cmd and "3661.55" in cmd for cmd in captured_cmds)
            return DiagnosticResult(5, "Seeking Precision", "PASS" if success else "FAIL", "Float precision verified for 3661.55s offset.")
        finally:
            subprocess.Popen = original_popen

    def run_all(self, stages: List[Any] = None) -> List[DiagnosticResult]:
        if not stages:
            stages = [
                self.level_1_seeking_injection, self.level_2_session_lifecycle,
                self.level_3_hw_acceleration, self.level_4_vlc_bridge_logic,
                self.level_5_seeking_precision
            ]
        return super().run_all(stages)

if __name__ == "__main__":
    PlayerSuiteEngine().run_all()
