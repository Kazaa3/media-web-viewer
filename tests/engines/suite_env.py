import sys
import os
from pathlib import Path
from typing import List

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

# Diagnostic Base
try:
    from tests.engines.test_base import DiagnosticEngine, DiagnosticResult
except ImportError:
    from test_base import DiagnosticEngine, DiagnosticResult

class EnvSuiteEngine(DiagnosticEngine):
    def __init__(self) -> None:
        super().__init__(suite_name="Env")

    def level_1_binary_check(self) -> DiagnosticResult:
        ffmpeg_exists = os.system("ffmpeg -version > /dev/null 2>&1") == 0
        ffprobe_exists = os.system("ffprobe -version > /dev/null 2>&1") == 0
        success = ffmpeg_exists and ffprobe_exists
        return DiagnosticResult(1, "Binary Check", "PASS" if success else "FAIL", "FFMPEG/FFPROBE binaries found.")

    def level_2_python_packages(self) -> DiagnosticResult:
        critical = ['psutil', 'bs4', 'eel', 'bottle', 'mutagen', 'pymediainfo', 'gevent', 'PIL', 'scapy']
        missing = []
        import importlib
        for pkg in critical:
            try:
                importlib.import_module(pkg)
            except ImportError:
                missing.append(pkg)
        
        success = not missing
        msg = f"Packages: {not missing}. Missing: {missing}" if missing else "All 9 core dependencies found."
        return DiagnosticResult(2, "Python Packages", "PASS" if success else "FAIL", msg)

    def level_3_deployment_assets(self) -> DiagnosticResult:
        pkg_root = PROJECT_ROOT / "packages"
        expected = ["src", "bin", "deb"]
        missing = [sd for sd in expected if not (pkg_root / sd).exists()]
        
        has_python = any((pkg_root / "src").glob("Python-*.tgz"))
        has_mtx = any((pkg_root / "bin").glob("mediamtx_*.tar.gz"))
        
        success = not missing and has_python and has_mtx
        msg = f"Reorganized structure: {not missing}. Archives: {has_python and has_mtx}."
        return DiagnosticResult(3, "Deployment Assets", "PASS" if success else "FAIL", msg)

    def run_all(self) -> List[DiagnosticResult]:
        stages = [self.level_1_binary_check, self.level_2_python_packages, self.level_3_deployment_assets]
        return super().run_all(stages)

if __name__ == "__main__":
    EnvSuiteEngine().run_all()
