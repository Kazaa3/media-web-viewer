import subprocess
import os
import logging
import shutil
from src.core.hardware_detector import get_best_hw_encoder # type: ignore

log = logging.getLogger("streams.hls_stream")

from typing import Dict, Any
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
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    encoder = get_best_hw_encoder()
    playlist_path = os.path.join(output_dir, "master.m3u8")

    log.info(f"[HLS] Starting {session_id} using {encoder} -> {playlist_path} (Audio:{audio_idx}, Subs:{subs_idx}, SS:{start_time})")

    # FFmpeg command for HLS fMP4
    # -ss before -i for fast input seeking
    cmd = [
        "ffmpeg",
        "-hide_banner", "-loglevel", "error",
        "-ss", str(float(start_time)),
        "-i", str(file_path),
        "-map", "0:v:0", # Map first video stream
        "-map", f"0:{audio_idx}", # Map selected audio stream (using global index from ffprobe)
    ]
    
    if subs_idx is not None and str(subs_idx).lower() != 'null':
        cmd += ["-map", f"0:{subs_idx}"]

    cmd += [
        "-c:v", encoder if encoder != "libx264" else "libx264",
        "-preset", "veryfast",
        "-c:a", "aac", "-b:a", "128k",
    ]

    # Handle Subtitles (experimental, often needs conversion to webvtt for HLS, 
    # but for now we try mapping text subs into the fMP4 container if supported)
    if subs_idx is not None:
         cmd += ["-c:s", "mov_text"] # fMP4 typically uses mov_text or webvtt

    cmd += [
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
