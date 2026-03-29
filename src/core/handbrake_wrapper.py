import subprocess
import os
import shutil
from typing import List, Dict, Any, Optional

class HandBrakeWrapper:
    """
    Python wrapper for HandBrakeCLI.
    Specializes in batch encoding and hardware acceleration (VAAPI/QSV).
    """

    def __init__(self):
        self.bin = shutil.which("HandBrakeCLI")

    def _run_command(self, cmd: List[str]) -> Dict[str, Any]:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def encode(self, input_path: str, output_path: str, preset: str = "Very Fast 1080p30", extra_args: List[str] = []) -> Dict[str, Any]:
        """Runs a standard encoding job."""
        if not self.bin:
            return {"success": False, "error": "HandBrakeCLI not found"}
        
        cmd = [
            self.bin,
            "-i", input_path,
            "-o", output_path,
            "--preset", preset
        ] + extra_args
        
        return self._run_command(cmd)

    def encode_vaapi(self, input_path: str, output_path: str) -> Dict[str, Any]:
        """Encodes with H.264 (Intel QSV / VAAPI) for speed."""
        return self.encode(input_path, output_path, preset="H.264 (Intel QSV) 1080p", extra_args=["--encoder", "vaapi_h264"])

    def get_presets(self) -> List[str]:
        """Lists available presets."""
        if not self.bin: return []
        res = self._run_command([self.bin, "--preset-list"])
        if res["success"]:
            # Basic parsing of preset list
            return [line.strip() for line in res["stdout"].splitlines() if line.startswith("    ")]
        return []

    def check_gpu(self) -> Dict[str, bool]:
        """Checks for hardware acceleration support."""
        if not self.bin: return {"vaapi": False, "qsv": False}
        res = self._run_command([self.bin, "--help"])
        help_text = res.get("stdout", "").lower()
        return {
            "vaapi": "vaapi" in help_text,
            "qsv": "qsv" in help_text
        }
