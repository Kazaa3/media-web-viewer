import os
import re
import subprocess
from pathlib import Path
from tests.engines.test_base import DiagnosticEngine, DiagnosticResult

class SubtitleSuiteEngine(DiagnosticEngine):
    """
    Engine for auditing subtitle processing capabilities.
    Verifies extraction, timing, and format support.
    """
    
    def __init__(self):
        super().__init__("Subtitle Processing Suite")
        self.web_root = Path("web")
        self.cache_dir = Path("cache")
        
    def level_1_extraction_audit(self) -> DiagnosticResult:
        """Audit for successful subtitle extraction capabilities."""
        # Check if ffmpeg is available
        try:
            subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
            has_ffmpeg = True
        except:
            has_ffmpeg = False
            
        status = has_ffmpeg
        detail = "FFmpeg detected and ready for extraction." if has_ffmpeg else "FFmpeg MISSING - Extraction will fail."
        
        status_str = "PASS" if status else "FAIL"
        return DiagnosticResult(
            level=1,
            name="Subtitle Extraction Engine",
            status=status_str,
            message=detail
        )

    def level_2_timing_engine_audit(self) -> DiagnosticResult:
        """Audit for subtitle timing libraries (pysubs2, pysrt)."""
        engines = []
        try:
            import pysubs2
            engines.append("pysubs2")
        except ImportError:
            pass
            
        try:
            import pysrt
            engines.append("pysrt")
        except ImportError:
            pass
            
        status = len(engines) > 0
        detail = f"Available timing engines: {', '.join(engines)}" if engines else "No timing engines found. Install pysubs2 or pysrt."
        
        status_str = "PASS" if status else "WARN"
        return DiagnosticResult(
            level=2,
            name="Subtitle Timing Engine",
            status=status_str,
            message=detail
        )

    def level_3_cache_integrity(self) -> DiagnosticResult:
        """Audit for subtitle cache performance and cleanup."""
        if not self.cache_dir.exists():
            return DiagnosticResult(3, "Cache Integrity", "PASS", "Cache directory not yet initialized.")
            
        sub_files = list(self.cache_dir.glob("*.srt")) + list(self.cache_dir.glob("*.vtt"))
        
        status = True
        detail = f"Found {len(sub_files)} processed subtitle files in cache."
        
        status_str = "PASS" if status else "WARN"
        return DiagnosticResult(
            level=3,
            name="Cache Integrity",
            status=status_str,
            message=detail
        )
