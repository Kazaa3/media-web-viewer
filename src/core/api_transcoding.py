import os
import time
import subprocess
import shutil
import threading
from pathlib import Path
from typing import Dict, Any, List, Optional, Generator

from src.core.config_master import (
    GLOBAL_CONFIG, PROJECT_ROOT, LOGS_DIR, 
    PROGRAM_REGISTRY, MEDIA_DIR
)
from src.core.logger import get_logger

log = get_logger("api_transcoding")

def get_best_hw_encoder() -> str:
    """
    Returns the best available hardware H.264 encoder (Forensic Performance v1.46.132).
    Priority: NVENC -> VAAPI -> QSV -> Software (libx264)
    """
    priority = GLOBAL_CONFIG.get("player_settings", {}).get("hardware_encoders_priority", ["nvenc", "vaapi", "qsv"])
    ffmpeg_path = PROGRAM_REGISTRY.get("ffmpeg", "ffmpeg")
    
    try:
        res = subprocess.run([ffmpeg_path, "-encoders"], capture_output=True, text=True, timeout=5)
        available = res.stdout if res.returncode == 0 else ""
        
        for enc in priority:
            if f"h264_{enc}" in available:
                log.info(f"[Transcoder] High-Performance Encoder Detected: {enc}")
                return f"h264_{enc}"
    except Exception as e:
        log.debug(f"[Transcoder] HW Discovery failed: {e}")
        
    return "libx264"

def is_mkvtoolnix_available() -> bool:
    """Checks if mkvmerge is available via the registry."""
    path = PROGRAM_REGISTRY.get("mkvmerge")
    return path is not None and os.path.exists(path)

def log_process_stderr(process: subprocess.Popen, name: str):
    """
    Streams process stderr to the master log and specialized files.
    """
    if not process or not process.stderr:
        return
    
    log_cfg = GLOBAL_CONFIG.get("logging_registry", {})
    enable_granular = log_cfg.get("enable_granular_transcoder_logs", False)
    log_dir = Path(log_cfg.get("transcoding_log_dir", str(LOGS_DIR / "transcoding")))
    
    log_handle = None
    if enable_granular:
        try:
            log_dir.mkdir(parents=True, exist_ok=True)
            log_file = log_dir / f"{name}_{int(time.time())}.log"
            log_handle = open(log_file, "a", encoding="utf-8")
        except Exception:
            pass

    def log_thread():
        try:
            for line in process.stderr:
                try:
                    decoded_line = line.decode(errors='replace').strip()
                    log.info(f" [{name}] {decoded_line}")
                    if log_handle:
                        log_handle.write(f"{time.strftime('%H:%M:%S')} - {decoded_line}\n")
                except Exception:
                    pass
        finally:
            if log_handle:
                try:
                    log_handle.close()
                except Exception:
                    pass

    threading.Thread(target=log_thread, daemon=True).start()

def get_transcode_stream(resolved_path: str, start_time: float = 0, 
                         audio_idx: int = 0, subs_idx: Optional[int] = None) -> Generator[bytes, None, None]:
    """
    Universal FFmpeg generator for real-time H.264/AAC FragMP4 streaming.
    """
    ffmpeg_path = PROGRAM_REGISTRY.get("ffmpeg", "ffmpeg")
    profiles = GLOBAL_CONFIG.get("transcoding_profiles", {})
    encoder = get_best_hw_encoder()
    
    low_path = str(resolved_path).lower()
    is_audio = any(ext in low_path for ext in GLOBAL_CONFIG.get("player_settings", {}).get("audio_extensions", []))
    
    cmd = [ffmpeg_path, "-hide_banner", "-loglevel", "error"]
    if start_time > 0:
        cmd.extend(["-ss", str(start_time)])
    
    cmd.extend(["-i", str(resolved_path)])
    
    if is_audio:
        profile = profiles.get("transcode_audio_aac", {}) # Default
        cmd.extend(["-vn", "-c:a", profile.get("codec", "aac"), "-b:a", profile.get("bitrate", "192k"), "-f", "mp4"])
    else:
        profile = profiles.get("video_transcode", {})
        if subs_idx is not None:
            cmd.extend(["-map", "0:v:0", "-map", f"0:a:{audio_idx}", "-map", f"0:s:{subs_idx}"])
        else:
            cmd.extend(["-map", "0:v:0", "-map", f"0:a:{audio_idx}"])
            
        cmd.extend([
            "-c:v", encoder, "-preset", profile.get("preset", "veryfast"), 
            "-crf", profile.get("crf", "23"),
            "-c:a", profile.get("a_codec", "aac"), "-b:a", profile.get("a_bitrate", "128k"),
            "-f", "mp4", "-movflags", "frag_keyframe+empty_moov+default_base_moof"
        ])
    
    cmd.append("pipe:1")
    
    perf_cfg = GLOBAL_CONFIG.get("perf_settings", {})
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                               bufsize=perf_cfg.get("streaming_buffer_size", 1024*1024))
    
    log_process_stderr(process, "FFmpeg-Stream")
    
    try:
        while True:
            chunk = process.stdout.read(512 * 1024)
            if not chunk: break
            yield chunk
    finally:
        if process:
            process.terminate()
            try: process.wait(timeout=1)
            except: process.kill()

def get_remux_stream(file_path: str, start_time: float = 0, 
                     audio_idx: int = 0, subs_idx: Optional[int] = None) -> Generator[bytes, None, None]:
    """
    Pipe-Kit generator: MKVMerge (Lossless) -> FFmpeg (FragMP4).
    """
    mkvmerge_path = PROGRAM_REGISTRY.get("mkvmerge", "mkvmerge")
    ffmpeg_path = PROGRAM_REGISTRY.get("ffmpeg", "ffmpeg")
    
    perf_cfg = GLOBAL_CONFIG.get("perf_settings", {})
    buf_size = perf_cfg.get("streaming_buffer_size", 1024*1024)
    
    # Seeking or track selection forces FFmpeg remux (more reliable than mkvmerge pipe for non-zero starts)
    if start_time > 0 or audio_idx > 0 or subs_idx is not None:
        cmd = [ffmpeg_path, "-loglevel", "error", "-ss", str(start_time), "-i", str(file_path)]
        cmd.extend(["-map", "0:v:0", "-map", f"0:a:{audio_idx}"])
        if subs_idx is not None: cmd.extend(["-map", f"0:s:{subs_idx}"])
        cmd.extend(["-c", "copy", "-f", "mp4", "-movflags", "frag_keyframe+empty_moov+default_base_moof", "pipe:1"])
        
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=buf_size)
        log_process_stderr(proc, "FFmpeg-Remux-SS")
        try:
            while True:
                chunk = proc.stdout.read(512 * 1024)
                if not chunk: break
                yield chunk
        finally:
            if proc: proc.terminate()
    else:
        # Full Pipe-Kit: MKVMerge -> FFmpeg
        mkv_proc = subprocess.Popen([mkvmerge_path, "-o", "-", str(file_path)], 
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=buf_size)
        ffmpeg_cmd = [ffmpeg_path, "-loglevel", "error", "-i", "pipe:0", "-c", "copy", 
                      "-f", "mp4", "-movflags", "frag_keyframe+empty_moov+default_base_moof", "-"]
        ff_proc = subprocess.Popen(ffmpeg_cmd, stdin=mkv_proc.stdout, 
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=buf_size)
        
        log_process_stderr(mkv_proc, "MKV-Pipe")
        log_process_stderr(ff_proc, "FFmpeg-Frag")
        
        try:
            while True:
                chunk = ff_proc.stdout.read(512 * 1024)
                if not chunk: break
                yield chunk
        finally:
            for p in [ff_proc, mkv_proc]:
                if p: p.terminate()
