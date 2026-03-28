import sys
import os
import shutil
import subprocess
from pathlib import Path
from typing import List, Dict, Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

# Try to import from relative path if inside the project
try:
    from tests.engines.test_base import DiagnosticEngine, DiagnosticResult
except ImportError:
    from test_base import DiagnosticEngine, DiagnosticResult

class ToolchainSuiteEngine(DiagnosticEngine):
    """
    Diagnostic suite for verifying the presence and health of external binaries.
    """

    def __init__(self) -> None:
        super().__init__(suite_name="Toolchain")

    def level_1_mkvtoolnix_presence(self) -> DiagnosticResult:
        """Verifies core MKVToolNix binaries."""
        tools = ["mkvmerge", "mkvextract", "mkvinfo", "mkvpropedit"]
        missing = [t for t in tools if not shutil.which(t)]
        
        if not missing:
            v = subprocess.run(["mkvmerge", "--version"], capture_output=True, text=True).stdout.strip()
            return DiagnosticResult(1, "MKVToolNix", "PASS", f"All tools found. {v}")
        return DiagnosticResult(1, "MKVToolNix", "FAIL", f"Missing: {', '.join(missing)}")

    def level_2_handbrake_presence(self) -> DiagnosticResult:
        """Verifies HandBrakeCLI presence and version."""
        hb = shutil.which("HandBrakeCLI")
        if hb:
            v = subprocess.run([hb, "--version"], capture_output=True, text=True).stdout.splitlines()[0]
            return DiagnosticResult(2, "HandBrakeCLI", "PASS", f"Found: {v}")
        return DiagnosticResult(2, "HandBrakeCLI", "FAIL", "HandBrakeCLI not found in PATH.")

    def level_3_ffplay_presence(self) -> DiagnosticResult:
        """Verifies ffplay presence."""
        ff = shutil.which("ffplay")
        if ff:
            v = subprocess.run([ff, "-version"], capture_output=True, text=True).stdout.splitlines()[0]
            return DiagnosticResult(3, "FFplay", "PASS", f"Found: {v}")
        return DiagnosticResult(3, "FFplay", "FAIL", "ffplay not found in PATH.")

    def level_4_swyh_rs_presence(self) -> DiagnosticResult:
        """Verifies swyh-rs-cli (Audio Streaming)."""
        sw = shutil.which("swyh-rs-cli")
        if sw:
            return DiagnosticResult(4, "SWYH-RS", "PASS", "Found: swyh-rs-cli")
        return DiagnosticResult(4, "SWYH-RS", "WARN", "swyh-rs-cli not found. Audio streaming might be limited.")

    def level_5_gpu_acceleration_check(self) -> DiagnosticResult:
        """Heuristic check for GPU transcoding support (VAAPI/QSV)."""
        hb = shutil.which("HandBrakeCLI")
        if not hb:
            return DiagnosticResult(5, "GPU Acceleration", "SKIP", "HandBrakeCLI missing.")
        
        res = subprocess.run([hb, "--help"], capture_output=True, text=True).stdout
        vaapi = "vaapi" in res.lower()
        qsv = "qsv" in res.lower()
        
        if vaapi or qsv:
            features = []
            if vaapi: features.append("VAAPI")
            if qsv: features.append("QSV")
            return DiagnosticResult(5, "GPU Acceleration", "PASS", f"Supported: {', '.join(features)}")
        return DiagnosticResult(5, "GPU Acceleration", "WARN", "No GPU acceleration detected via HandBrake CLI help.")

    def level_10_integrity(self) -> DiagnosticResult:
        """Verifies DB and Debugging/Logging infrastructure."""
        try:
            from src.core import db
            from src.core import logger
            
            # 1. Logger Verification
            log = logger.get_logger("test_integrity")
            log.info("Integrity check running.")
            
            # 2. DB Verification (Active)
            handler = db.DatabaseHandler()
            stats = handler.get_db_stats()
            
            db_ok = stats.get("total_items", -1) >= 0
            log_ok = hasattr(logger, "get_logger")
            
            if db_ok and log_ok:
                return DiagnosticResult(10, "Integrity System", "PASS", f"DB Verified ({stats.get('total_items')} items), Logger active.")
            return DiagnosticResult(10, "Integrity System", "WARN", f"DB healthy: {db_ok}, Log: {log_ok}")
        except Exception as e:
            return DiagnosticResult(10, "Integrity System", "FAIL", str(e))

    def run_all(self, stages: List[Any] = None) -> List[DiagnosticResult]:
        if not stages:
            stages = [
                self.level_1_mkvtoolnix_presence,
                self.level_2_handbrake_presence,
                self.level_3_ffplay_presence,
                self.level_4_swyh_rs_presence,
                self.level_5_gpu_acceleration_check,
                self.level_10_integrity
            ]
        return super().run_all(stages)

if __name__ == "__main__":
    engine = ToolchainSuiteEngine()
    engine.run_all()
