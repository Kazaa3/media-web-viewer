import sys
import os
from pathlib import Path
from typing import List

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

# Diagnostic Base
try:
    from tests.test_base import DiagnosticEngine, DiagnosticResult
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
        try:
            import psutil
            import bs4
            success = True
        except ImportError:
            success = False
        return DiagnosticResult(2, "Python Packages", "PASS" if success else "WARN", "Core dependencies checked.")

    def run_all(self) -> List[DiagnosticResult]:
        stages = [self.level_1_binary_check, self.level_2_python_packages]
        return super().run_all(stages)

if __name__ == "__main__":
    EnvSuiteEngine().run_all()
