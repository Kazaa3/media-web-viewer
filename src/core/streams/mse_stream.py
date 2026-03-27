import subprocess
import os
import logging
import threading
import time
from src.core.hardware_detector import get_best_hw_encoder # type: ignore

log = logging.getLogger("streams.mse_stream")

# Global dict to track active streaming processes
ACTIVE_STREAMS = {}

def start_mse_stream(file_path, stream_id, audio_idx=0, subs_idx=None, start_time=0):
    """
    @brief Starts an FFmpeg process to remux media into Fragmented MP4 for MSE.
    @details Supports fast seeking (-ss before -i) and track mapping.
    @param file_path Path to the source file.
    @param stream_id Unique identifier for the stream session.
    @param audio_idx Index of the audio track to map.
    @param subs_idx Index of the subtitle track to map (if any).
    @param start_time Seek position in seconds.
    @return subprocess.Popen instance.
    """
    if not os.path.exists(file_path):
        log.error(f"[MSE] File not found: {file_path}")
        return None

    # Stop existing stream for this ID if any
    stop_mse_stream(stream_id)

    encoder = get_best_hw_encoder()
    log.info(f"[MSE] Starting stream {stream_id} (Seek: {start_time}s, Audio: {audio_idx}) using {encoder}")

    # FFmpeg command for FragMP4 remuxing
    # -ss BEFORE -i for fast seeking
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error"]
    
    if float(start_time) > 0:
        cmd.extend(["-ss", str(start_time)])
        
    cmd.extend(["-i", str(file_path)])
    
    # Mapping
    cmd.extend(["-map", "0:v:0"]) # Always first video track
    cmd.extend(["-map", f"0:a:{audio_idx}"])
    if subs_idx is not None:
        cmd.extend(["-map", f"0:s:{subs_idx}"])
    
    # Encoding / Remuxing
    cmd.extend([
        "-c:v", encoder if encoder != "libx264" else "libx264",
        "-preset", "ultrafast",
        "-tune", "zerolatency",
        "-c:a", "aac", "-b:a", "128k",
        "-f", "mp4",
        "-movflags", "frag_keyframe+empty_moov+default_base_moof",
        "pipe:1"
    ])

    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ACTIVE_STREAMS[stream_id] = process
        
        # Start a cleanup thread
        threading.Thread(target=_monitor_process, args=(stream_id, process), daemon=True).start()
        
        return process
    except Exception as e:
        log.error(f"[MSE] Failed to start FFmpeg: {e}")
        return None

def _monitor_process(stream_id, process):
    """Monitors and cleans up the FFmpeg process."""
    process.wait()
    ACTIVE_STREAMS.pop(stream_id, None)
    log.info(f"[MSE] Stream {stream_id} terminated.")

def stop_mse_stream(stream_id):
    """Stops an active MSE stream."""
    if stream_id in ACTIVE_STREAMS:
        process = ACTIVE_STREAMS.pop(stream_id, None)
        if hasattr(process, "terminate"):
            process.terminate()
            try:
                process.wait(timeout=2)
            except:
                process.kill()
        return True
    return False
