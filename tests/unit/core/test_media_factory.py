import subprocess
import os
from pathlib import Path
import logging

log = logging.getLogger("test_factory")

def generate_mock_media(target_dir, filename, type="video", codec="h264", duration=1):
    """
    @brief Generates a valid minimal media file using FFmpeg for testing.
    @param target_dir Where to save the file.
    @param filename Name of the file (e.g. 'test.mp4').
    @param type 'video' or 'audio'.
    @param codec 'h264', 'hevc', 'vp9', 'mp3', 'flac'.
    @param duration Duration in seconds.
    """
    out_path = Path(target_dir) / filename
    out_path.parent.mkdir(parents=True, exist_ok=True)
    
    if out_path.exists():
        return str(out_path)
        
    log.info(f"Generating mock {type} ({codec}): {out_path}")
    
    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    
    if type == "video":
        # Generate 1 frame/sec test video with color pattern
        cmd += ["-f", "lavfi", "-i", f"testsrc=duration={duration}:size=1280x720:rate=1"]
        if codec == "h264":
            cmd += ["-c:v", "libx264", "-pix_fmt", "yuv420p"]
        elif codec == "hevc":
            cmd += ["-c:v", "libx265", "-pix_fmt", "yuv420p"]
        elif codec == "vp9":
            cmd += ["-c:v", "libvpx-vp9"]
        else:
            cmd += ["-c:v", "copy"] # fallback
            
        # Add silent audio if video
        cmd += ["-f", "lavfi", "-i", f"anullsrc=duration={duration}", "-c:a", "aac", "-shortest"]
        
    elif type == "audio":
        cmd += ["-f", "lavfi", "-i", f"sine=duration={duration}:frequency=440"]
        if codec == "mp3":
            cmd += ["-c:a", "libmp3lame"]
        elif codec == "flac":
            cmd += ["-c:a", "flac"]
        elif codec == "opus":
            cmd += ["-c:a", "libopus"]
        else:
            cmd += ["-c:a", "pcm_s16le"]
            
    cmd.append(str(out_path))
    
    try:
        subprocess.run(cmd, check=True)
        return str(out_path)
    except Exception as e:
        log.error(f"Failed to generate mock media: {e}")
        return None

def prepare_test_suite_files(media_dir):
    """Generates a full matrix of test files."""
    files = {
        "native_mp4_h264": ("h264_aac.mp4", "video", "h264"),
        "non_native_mp4_h265": ("h265_aac.mp4", "video", "hevc"),
        "non_native_mkv_h264": ("h264_aac.mkv", "video", "h264"),
        "native_webm_vp9": ("vp9_opus.webm", "video", "vp9"),
        "native_audio_mp3": ("sine.mp3", "audio", "mp3"),
        "non_native_audio_flac": ("sine.flac", "audio", "flac"),
        "native_audio_opus": ("sine.opus", "audio", "opus"),
    }
    
    results = {}
    for key, (fname, t, c) in files.items():
        results[key] = generate_mock_media(media_dir, fname, t, c)
    return results
