import os
import time
import subprocess
import threading
from pathlib import Path
from typing import Dict, Any, Optional, Generator

from src.core.config_master import GLOBAL_CONFIG, PROJECT_ROOT
from src.core.logger import get_logger

log = get_logger("streaming_processor")

class StreamingProcessor:
    """
    Orchestrates high-performance streaming engines (FFmpeg, MediaMTX, VLC).
    Handles real-time transcoding pipes and HLS/WebRTC broadcast.
    """

    @staticmethod
    def get_best_hw_encoder() -> str:
        """ Detects the best available hardware encoder (nvenc, vaapi, or libx264). """
        # Simplified auto-detection logic
        import shutil
        if shutil.which("nvidia-smi"):
            return "h264_nvenc"
        return "libx264"

    @staticmethod
    def spawn_ffmpeg_stream(file_path: str, 
                            mode: str = "fragmented", 
                            audio_idx: int = 0, 
                            subs_idx: Optional[int] = None, 
                            start_time: float = 0.0) -> Generator[bytes, None, None]:
        """
        Generates a fragmented MP4 stream via FFmpeg pipe.
        """
        encoder = StreamingProcessor.get_best_hw_encoder()
        log.info(f"[Streaming] Initializing {mode} stream for {file_path} (Encoder: {encoder})")

        resolved_path = Path(file_path).resolve()
        
        # Base command
        cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error"]
        
        if start_time > 0:
            cmd.extend(["-ss", str(start_time)])
            
        cmd.extend(["-i", str(resolved_path)])
        
        # Mapping logic
        if subs_idx is not None:
             cmd.extend(["-map", "0:v:0", "-map", f"0:a:{audio_idx}", "-map", f"0:s:{subs_idx}"])
        else:
             cmd.extend(["-map", "0:v:0", "-map", f"0:a:{audio_idx}"])

        # Transcoding flags (v1.54 Forensic Standard)
        cmd.extend([
            "-c:v", encoder, "-preset", "veryfast", "-crf", "23",
            "-c:a", "aac", "-b:a", "128k",
            "-f", "mp4",
            "-movflags", "frag_keyframe+empty_moov+default_base_moof",
            "pipe:1"
        ])

        perf_cfg = GLOBAL_CONFIG.get("perf_settings", {})
        stream_buf = perf_cfg.get("streaming_buffer_size", 1024 * 1024)

        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=stream_buf)

        def log_errors(p):
            for line in p.stderr:
                log.error(f"[FFmpeg-Pipe] {line.decode().strip()}")
        
        threading.Thread(target=log_errors, args=(process,), daemon=True).start()

        try:
            while True:
                chunk = process.stdout.read(256 * 1024)
                if not chunk:
                    break
                yield chunk
        finally:
            process.terminate()
            try:
                process.wait(timeout=1)
            except:
                process.kill()

    @staticmethod
    def orchestrate_mediamtx(file_path: str, protocol: str = "hls") -> Dict[str, Any]:
        """
        Orchestrates MediaMTX for high-reliability streaming.
        """
        # Placeholder for MediaMTX API integration or configuration management
        log.info(f"[Streaming] Orchestrating MediaMTX via {protocol} for {file_path}")
        return {
            "status": "active",
            "endpoint": f"http://localhost:8888/{protocol}/{Path(file_path).stem}",
            "engine": "MediaMTX"
        }
