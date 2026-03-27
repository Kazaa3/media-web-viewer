import subprocess
import logging
import bottle
import os
import shutil
from pathlib import Path
from .utils import get_best_ffmpeg_encoder, get_base_ffmpeg_args, get_video_filter
from src.core.ffprobe_analyzer import ffprobe_analyze

# Specialized logger
log = logging.getLogger("streams.hls")

def setup_hls_stream(file_path, audio_idx=0, subs_idx=None, start_time=0):
    """
    @brief Initializes an HLS fMP4 stream.
    @details Generates an M3U8 playlist and fMP4 segments in a temporary directory.
    @param file_path Path to the source file.
    @return URL to the generated playlist.
    """
    analysis = ffprobe_analyze(file_path)
    output_dir = Path("/tmp/mwv_hls") / f"{hash(str(file_path))}"
    if output_dir.exists(): shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    playlist_path = output_dir / "playlist.m3u8"
    
    encoder = get_best_ffmpeg_encoder()
    cmd = get_base_ffmpeg_args(encoder)
    
    if float(start_time or 0) > 0:
        cmd += ["-ss", str(start_time)]

    cmd += ["-i", str(file_path)]
    cmd += ["-map", "0:v:0", "-map", f"0:a:{audio_idx}"]
    
    is_4k = analysis.get("resolution") == "4K"
    vf = get_video_filter(analysis, subs_idx, is_4k)
    
    # Encoder tuning (similar to MSE but with HLS output)
    if encoder == "h264_vaapi":
        vf.insert(0, "format=nv12,hwupload")
        cmd += ["-vf", ",".join(vf), "-c:v", "h264_vaapi", "-b:v", "12M" if is_4k else "6M"]
    elif encoder == "h264_nvenc":
        if vf: cmd += ["-vf", ",".join(vf)]
        cmd += ["-c:v", "h264_nvenc", "-preset", "p1", "-rc", "vbr", "-cq", "24"]
    else:
        if vf: cmd += ["-vf", ",".join(vf)]
        cmd += ["-c:v", "libx264", "-preset", "ultrafast", "-crf", "26"]

    # HLS Specific flags for fMP4
    cmd += [
        "-c:a", "aac", "-b:a", "128k",
        "-f", "hls",
        "-hls_time", "2",
        "-hls_list_size", "0",
        "-hls_segment_type", "fmp4",
        "-hls_flags", "delete_segments+independent_segments",
        str(playlist_path)
    ]
    
    log.info(f"[HLS-Stream] Starting background HLS generation: {' '.join(cmd)}")
    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Return the relative URL that the frontend will use
    return f"/hls_tmp/{output_dir.name}/playlist.m3u8"

def serve_hls_segment(path):
    """
    @brief Bottle route handler for HLS segments and playlists.
    """
    return bottle.static_file(path, root="/tmp/mwv_hls")
