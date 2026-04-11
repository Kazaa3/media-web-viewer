import subprocess
import json
import os
import shutil
from typing import List, Dict, Any, Optional

class MKVToolWrapper:
    """
    High-level Python wrapper for MKVToolNix CLI utilities.
    Requires 'mkvmerge', 'mkvextract', 'mkvinfo', and 'mkvpropedit' to be in PATH.
    """

    def __init__(self):
        self.mkvmerge = shutil.which("mkvmerge")
        self.mkvextract = shutil.which("mkvextract")
        self.mkvinfo = shutil.which("mkvinfo")
        self.mkvpropedit = shutil.which("mkvpropedit")

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

    def get_info(self, mkv_path: str) -> Dict[str, Any]:
        """Runs mkvmerge --identify (JSON) for deep inspection."""
        if not self.mkvmerge:
            return {"success": False, "error": "mkvmerge not found"}
        
        cmd = [self.mkvmerge, "--identify", "--identification-format", "json", mkv_path]
        res = self._run_command(cmd)
        if res["success"]:
            try:
                return {"success": True, "data": json.loads(res["stdout"])}
            except json.JSONDecodeError:
                return {"success": False, "error": "Failed to parse mkvmerge JSON output"}
        return res

    def extract_track(self, mkv_path: str, track_id: int, output_path: str) -> Dict[str, Any]:
        """Extracts a specific track (audio/sub/video) to a file."""
        if not self.mkvextract:
            return {"success": False, "error": "mkvextract not found"}
        
        # Format: mkvextract <mkv> tracks <track_id>:<output>
        cmd = [self.mkvextract, mkv_path, "tracks", f"{track_id}:{output_path}"]
        return self._run_command(cmd)

    def mux_mkv(self, output_path: str, inputs: List[str], options: List[str] = []) -> Dict[str, Any]:
        """Muxes multiple inputs into a single MKV file."""
        if not self.mkvmerge:
            return {"success": False, "error": "mkvmerge not found"}
        
        cmd = [self.mkvmerge, "-o", output_path] + options + inputs
        return self._run_command(cmd)

    def edit_properties(self, mkv_path: str, edits: List[str]) -> Dict[str, Any]:
        """
        Edits MKV metadata/tags via mkvpropedit.
        Example edits: ["--set", "title=New Movie", "--edit", "track:s1", "--set", "language=ger"]
        """
        if not self.mkvpropedit:
            return {"success": False, "error": "mkvpropedit not found"}
        
        cmd = [self.mkvpropedit, mkv_path] + edits
        return self._run_command(cmd)

    def check_tools(self) -> Dict[str, bool]:
        """Returns availability status of all tools."""
        return {
            "mkvmerge": bool(self.mkvmerge),
            "mkvextract": bool(self.mkvextract),
            "mkvinfo": bool(self.mkvinfo),
            "mkvpropedit": bool(self.mkvpropedit)
        }
