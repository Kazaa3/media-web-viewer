#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path

# Create a test media directory
dest_dir = Path("media/test_files")
dest_dir.mkdir(parents=True, exist_ok=True)

# Generate a valid 2-second MP4 video
print("Generating valid MP4...")
subprocess.run([
    "ffmpeg", "-y", "-f", "lavfi", "-i", "testsrc=duration=2:size=640x360:rate=30",
    "-c:v", "libx264", "-pix_fmt", "yuv420p",
    str(dest_dir / "valid_test.mp4")
], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Generate a valid MKV video
print("Generating valid MKV...")
subprocess.run([
    "ffmpeg", "-y", "-f", "lavfi", "-i", "testsrc=duration=2:size=640x360:rate=30",
    "-c:v", "libx264", "-pix_fmt", "yuv420p",
    str(dest_dir / "valid_test.mkv")
], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Generate a mock DVD structure
dvd_dir = dest_dir / "TestMovie (2024) - DVD"
dvd_dir.mkdir(exist_ok=True)
iso_path = dvd_dir / "TestMovie (2024).iso"
if not iso_path.exists():
    print("Generating pure mock ISO...")
    with open(iso_path, "wb") as f:
        f.write(b"MOCK_ISO_DATA_DONT_PLAY")

print("\nFinished generating real dummy files.")
