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
        binaries = {
            "ffmpeg": "ffmpeg -version",
            "ffprobe": "ffprobe -version",
            "ffplay": "ffplay -version",
            "mkvmerge": "mkvmerge --version",
            "vlc": "vlc --version",
            "mpv": "mpv --version",
            "swyh-rs": "swyh-rs --help"
        }
        missing = []
        for name, cmd in binaries.items():
            if os.system(f"{cmd} > /dev/null 2>&1") != 0:
                missing.append(name)
        
        success = not missing
        return DiagnosticResult(1, "Binary Check", "PASS" if success else "WARN", 
                                f"Missing: {missing}" if missing else "All 7 media binaries found.")

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

    def level_4_legacy_build_integrity(self) -> DiagnosticResult:
        """Verifies the presence and size of legacy build artifacts in dist/."""
        dist_dir = PROJECT_ROOT / "dist"
        if not dist_dir.exists():
            return DiagnosticResult(4, "Legacy Build Integrity", "SKIP", "Dist directory missing.")
        
        builds = list(dist_dir.glob("MediaWebViewer*"))
        large_builds = [b for b in builds if b.stat().st_size > 100 * 1024 * 1024]
        
        status = "PASS" if len(large_builds) >= 1 else "WARN"
        return DiagnosticResult(4, "Legacy Build Integrity", status, f"Found {len(large_builds)} valid legacy build artifacts (>100MB).")

    def level_5_test_artifacts_audit(self) -> DiagnosticResult:
        """Verifies presence of generated test media (Legacy: test_file_formats_suite.py)."""
        artifacts_dir = PROJECT_ROOT / "tests" / "artifacts" / "real_media"
        if not artifacts_dir.exists():
            return DiagnosticResult(5, "Test Artifacts", "WARN", "real_media directory missing (run generate_test_media.py).")
        
        files = list(artifacts_dir.glob("*"))
        status = "PASS" if len(files) >= 5 else "WARN"
        return DiagnosticResult(5, "Test Artifacts", status, f"Found {len(files)} test media files.")

    def level_6_python_version_audit(self) -> DiagnosticResult:
        """Verifies Python runtime version (Legacy: test_python_version.py)."""
        import sys
        v = sys.version_info
        success = v.major == 3 and v.minor >= 10
        return DiagnosticResult(6, "Python Version", "PASS" if success else "WARN", f"Running on Python {v.major}.{v.minor}.{v.micro}")

if __name__ == "__main__":
    EnvSuiteEngine().run_all()
