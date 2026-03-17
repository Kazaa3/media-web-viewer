#!/usr/bin/env python3
"""
Generates minimal, real video containers for integration and E2E testing
without bloating the repository. Requires ffmpeg and genisoimage.
"""

import os
import shutil
import subprocess
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def generate_real_test_media(output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if not shutil.which("ffmpeg"):
        logging.error("ffmpeg is required but not installed in PATH.")
        return False
        
    # Define formats and basic codecs that fit the container
    FORMATS = {
        "mp4": ["-c:v", "libx264", "-c:a", "aac"],
        "mkv": ["-c:v", "libx264", "-c:a", "aac"],
        "webm": ["-c:v", "libvpx", "-c:a", "libvorbis"],
        "avi": ["-c:v", "mpeg4", "-c:a", "mp3"],
        "ts": ["-c:v", "libx264", "-c:a", "aac"]
    }
    
    success = True
    for ext, codecs in FORMATS.items():
        out_file = output_dir / f"test_video.{ext}"
        if not out_file.exists():
            # 1 second of colorbars and 440Hz sine wave beep
            cmd = [
                "ffmpeg", "-y",
                "-f", "lavfi", "-i", "testsrc=duration=1:size=640x360:rate=30",
                "-f", "lavfi", "-i", "sine=frequency=440:duration=1",
            ] + codecs + [str(out_file)]
            
            try:
                subprocess.run(cmd, check=True, capture_output=True)
                logging.info(f"Generated {out_file.name}")
            except subprocess.CalledProcessError as e:
                logging.error(f"Failed to generate {ext}: {e.stderr.decode('utf-8', errors='ignore')}")
                success = False
        else:
            logging.info(f"{out_file.name} already exists.")
                
    # Generate a dummy ISO if genisoimage is available
    iso_tool = shutil.which("genisoimage") or shutil.which("mkisofs")
    if iso_tool:
        dvd_dir = output_dir / "dvd_structure"
        dvd_dir.mkdir(exist_ok=True)
        video_ts = dvd_dir / "VIDEO_TS"
        video_ts.mkdir(exist_ok=True)
        # Create a fake IFO file so detection logic is triggered
        with open(video_ts / "VIDEO_TS.IFO", "wb") as f:
            f.write(b"DVDVIDEO-VTS") 
            
        iso_file = output_dir / "test_dvd.iso"
        if not iso_file.exists():
            try:
                subprocess.run([iso_tool, "-quiet", "-o", str(iso_file), str(dvd_dir)], check=True, capture_output=True)
                logging.info(f"Generated {iso_file.name}")
            except subprocess.CalledProcessError as e:
                logging.error(f"Failed to generate ISO: {e.stderr.decode('utf-8', errors='ignore')}")
                success = False
        else:
            logging.info(f"{iso_file.name} already exists.")
    else:
        logging.warning("genisoimage or mkisofs not found; skipping ISO generation.")
        
    return success

if __name__ == "__main__":
    out_path = Path(__file__).parent.parent / "artifacts" / "real_media"
    success = generate_real_test_media(out_path)
    if not success:
        exit(1)
