import os
import sys
import time
import subprocess
from pathlib import Path

# Dynamic Path Discovery (v1.46.132)
from src.core.config_master import PROJECT_ROOT, DB_FILENAME, TEST_DIR, DATA_DIR

# Attempt to load config (v1.35.98 SSOT)
try:
    from src.core.config_master import GLOBAL_CONFIG
except ImportError:
    print("[Error] Could not load config_master.py. Check sys.path.")
    sys.exit(1)

def build_test_command(file_path):
    resolved_path = PROJECT_ROOT / file_path
    if not resolved_path.exists():
        return None, None, f"[Error] File not found: {file_path}"

    # Identification (Mock logic from main.py)
    low_path = file_path.lower()
    audio_exts = GLOBAL_CONFIG.get("player_settings", {}).get("audio_extensions", [])
    is_audio = any(ext in low_path for ext in audio_exts)
    is_iso = low_path.endswith('.iso')
    profiles = GLOBAL_CONFIG.get("transcoding_profiles", {})
    
    # Profile selection
    p_key = "video_transcode"
    if is_audio:
        p_key = "transcode_audio_aac"
        if ".opus" in low_path: p_key = "transcode_audio_opus"
        elif ".alac" in low_path or ".m4a" in low_path: p_key = "transcode_audio_flac"
        elif ".wma" in low_path: p_key = "transcode_audio_wma"
    
    profile = profiles.get(p_key, {})
    
    # Command Construction (v1.35.98 Logic)
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(resolved_path)]
    if is_audio:
        codec = profile.get("codec", "aac")
        bitrate = profile.get("bitrate", "128k")
        fmt = profile.get("format", "mp4")
        cmd.extend(["-vn", "-c:a", codec, "-b:a", bitrate, "-f", fmt])
        if profile.get("movflags"):
            cmd.extend(["-movflags", profile.get("movflags")])
    else:
        # Video/ISO logic
        preset = profile.get("preset", "veryfast")
        crf = profile.get("crf", "23")
        a_codec = profile.get("a_codec", "aac")
        fmt = profile.get("format", "mp4")
        cmd.extend(["-c:v", "libx264", "-preset", preset, "-crf", crf, "-c:a", a_codec, "-f", fmt])
        if profile.get("movflags"):
            cmd.extend(["-movflags", profile.get("movflags")])
            
    cmd.extend(["-t", "0.5", "-f", "null", "-"]) # Test only 0.5s output
    return cmd, p_key, None

def run_suite():
    tests = [
        ("WMA TRANSCODE", "media/03_deichkind_-_remmidemmi_(yippie_yippie_yeah).wma"),
        ("ALAC TRANSCODE", "media/01-02-Oscar_Peterson-Easy_Does_It-LLS.m4a"),
        ("VIDEO TRANSCODE", "media/572c61da1d0249d0613070a2a3113f8c.mp4"),
        ("ISO TRANSCODE", "media/Going Raw - JUDITA_169_OPTION.ISO")
    ]

    print("=== Transcoding Test Suite (v1.35.98) ===\n")
    for name, path in tests:
        print(f"[{name}] {path}")
        cmd, profile, err = build_test_command(path)
        
        if err:
            print(f"  {err}")
            continue
            
        print(f"  Profile: {profile}")
        print(f"  Command: {' '.join(cmd)}")
        
        # Non-blocking Execution with Timeout
        try:
            # Capture both stdout/stderr. Timeout is STRICT 5s.
            proc = subprocess.run(cmd, capture_output=True, timeout=5)
            if proc.returncode == 0:
                print(f"  [SUCCESS] FFmpeg initialized and processed header correctly.")
            else:
                stderr = proc.stderr.decode().strip()
                print(f"  [FAILURE] FFmpeg error: {stderr[:150]}...")
        except subprocess.TimeoutExpired:
            print("  [TIMEOUT] FFmpeg took longer than 5s (disk/IO wait).")
        except Exception as e:
            print(f"  [ERROR] {e}")
        print("-" * 60)

if __name__ == "__main__":
    run_suite()
