import subprocess
import os
import logging
import shutil
from src.core.hardware_detector import get_best_hw_encoder # type: ignore

log = logging.getLogger("streams.hls_stream")

# Global dict to track active HLS sessions
HLS_SESSIONS = {}

def start_hls_fmp4(file_path, output_dir, session_id):
    """
    @brief Starts an FFmpeg process for universal HLS (fMP4) streaming.
    @details High compatibility across all Apple and modern Android/Web clients.
    @param file_path Source path.
    @param output_dir Directory where the playlist and segments are stored.
    @param session_id Unique identifier.
    @return subprocess.Popen instance.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    encoder = get_best_hw_encoder()
    playlist_path = os.path.join(output_dir, "master.m3u8")

    log.info(f"[HLS] Starting {session_id} using {encoder} -> {playlist_path}")

    # FFmpeg command for HLS fMP4
    # -hls_segment_type fmp4 for modern HLS
    # -hls_flags delete_segments to save disk space
    cmd = [
        "ffmpeg",
        "-hide_banner", "-loglevel", "error",
        "-i", str(file_path),
        "-c:v", encoder if encoder != "libx264" else "libx264",
        "-preset", "veryfast",
        "-c:a", "aac", "-b:a", "128k",
        "-f", "hls",
        "-hls_time", "6", # 6 second segments
        "-hls_list_size", "10", # Keep 10 segments in playlist
        "-hls_segment_type", "fmp4",
        "-hls_flags", "delete_segments+independent_segments",
        "-hls_segment_filename", os.path.join(output_dir, "seg_%d.m4s"),
        playlist_path
    ]

    try:
        process = subprocess.Popen(cmd)
        HLS_SESSIONS[session_id] = {
            "process": process,
            "output_dir": output_dir,
            "playlist": playlist_path
        }
        return process
    except Exception as e:
        log.error(f"[HLS] Failed to start session {session_id}: {e}")
        return None

def stop_hls_fmp4(session_id):
    """Stops HLS and cleans up segments."""
    session = HLS_SESSIONS.pop(session_id, None)
    if session and "process" in session:
        process = session["process"]
        if process: # Ensure process is not None
            if hasattr(process, "terminate"):
                process.terminate()
                try:
                    process.wait(timeout=3)
                except:
                    process.kill()
        
        # Cleanup segments
        output_dir = session.get("output_dir")
        if output_dir and os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        return True
    return False
