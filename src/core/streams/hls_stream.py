import subprocess
import os
import shutil
from pathlib import Path
from src.core.hardware_detector import get_best_hw_encoder # type: ignore
from src.core.logger import get_logger
from src.core.config_master import GLOBAL_CONFIG
from src.core.streams.utils import get_base_ffmpeg_args

log = get_logger("streams_hls")

from typing import Dict, Any, Optional
# Global dict to track active HLS sessions
HLS_SESSIONS: Dict[str, Dict[str, Any]] = {}

def start_hls_fmp4(file_path, output_dir, session_id, audio_idx=0, subs_idx=None, start_time=0):
    """
    @brief Starts an FFmpeg process for universal HLS (fMP4) streaming.
    @details High compatibility across all Apple and modern Android/Web clients.
    @param file_path Source path.
    @param output_dir Directory where the playlist and segments are stored.
    @param session_id Unique identifier.
    @param audio_idx Select specific audio track index.
    @param subs_idx Select specific subtitle track index (None if off).
    @param start_time Seek to position in seconds.
    @return subprocess.Popen instance.
    """
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    
    encoder = get_best_hw_encoder()
    playlist_path = out_path / "master.m3u8"

    # Pull configuration (Phase 9 Centralization)
    reg = GLOBAL_CONFIG.get("media_pipeline_registry", {}).get("video", {})
    hls_cfg = reg.get("streaming_params", {}).get("hls", {})
    
    hls_time = hls_cfg.get("segment_time", "6")
    hls_list_size = hls_cfg.get("list_size", "10")

    log.info(f"[HLS] Starting {session_id} using {encoder} -> {playlist_path} (A:{audio_idx}, S:{subs_idx}, T:{start_time})")

    # Use centralized base args (v1.46.132)
    cmd = get_base_ffmpeg_args(encoder)
    
    # Assembly
    cmd += [
        "-ss", str(float(start_time)),
        "-i", str(file_path),
        "-map", "0:v:0", 
        "-map", f"0:{audio_idx}",
    ]
    
    if subs_idx is not None and str(subs_idx).lower() != 'null':
        cmd += ["-map", f"0:{subs_idx}"]

    cmd += [
        "-c:v", encoder if encoder != "libx264" else "libx264",
        "-preset", "veryfast",
        "-c:a", "aac", "-b:a", "128k",
    ]

    if subs_idx is not None:
         cmd += ["-c:s", "mov_text"]

    cmd += [
        "-f", "hls",
        "-hls_time", str(hls_time),
        "-hls_list_size", str(hls_list_size),
        "-hls_segment_type", "fmp4",
        "-hls_flags", "delete_segments+independent_segments",
        "-hls_segment_filename", str(out_path / "seg_%d.m4s"),
        str(playlist_path)
    ]

    try:
        process = subprocess.Popen(cmd)
        HLS_SESSIONS[session_id] = {
            "process": process,
            "output_dir": str(out_path),
            "playlist": str(playlist_path)
        }
        return process
    except Exception as e:
        log.error(f"[HLS] Failed to start session {session_id}: {e}", exc_info=True)
        return None

def stop_hls_fmp4(session_id):
    """Stops HLS and cleans up segments."""
    session = HLS_SESSIONS.pop(session_id, None)
    if session and "process" in session:
        process = session["process"]
        if process:
            if hasattr(process, "terminate"):
                process.terminate()
                try:
                    process.wait(timeout=3)
                except:
                    process.kill()
        
        output_dir = session.get("output_dir")
        if output_dir and os.path.exists(output_dir):
            try:
                shutil.rmtree(output_dir)
            except Exception as e:
                log.debug(f"[HLS] Cleanup failed for {output_dir}: {e}")
        return True
    return False

