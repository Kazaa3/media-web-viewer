#!/usr/bin/env python3
import subprocess
import os
from pathlib import Path

def generate_mock_video(output_path, codec="h264", container="mp4", duration=5, label="Mock"):
    """Generates a small mock video using ffmpeg."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", f"testsrc=duration={duration}:size=640x360:rate=30",
        "-f", "lavfi", "-i", f"sine=frequency=1000:duration={duration}",
        "-c:v", "libx264" if codec == "h264" else "libvpx-vp9",
        "-c:a", "aac" if container != "webm" else "libopus",
        "-pix_fmt", "yuv420p",
        str(output_path)
    ]
    
    if container == "mkv":
        cmd[-1] = str(output_path.with_suffix(".mkv"))
    elif container == "webm":
        cmd[-1] = str(output_path.with_suffix(".webm"))
    
    print(f"Generating {output_path}...")
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def generate_mock_iso(output_path, label="MockISO"):
    """Generates a mock DVD ISO (just a file with .iso extension)."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(b"Mock ISO Content " * 1024)
    print(f"Generated {output_path}")

def main():
    media_dir = Path("/home/xc/#Coding/gui_media_web_viewer/media/mock_files")
    media_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate various formats
    generate_mock_video(media_dir / "vortrag_mock.mp4", codec="h264", container="mp4", label="Vortrag Mock")
    generate_mock_video(media_dir / "test.mkv", codec="h264", container="mkv", label="MKV H264")
    generate_mock_video(media_dir / "test_vp9.mkv", codec="vp9", container="mkv", label="MKV VP9")
    generate_mock_video(media_dir / "test.webm", codec="vp9", container="webm", label="WebM")
    
    generate_mock_iso(media_dir / "test_movie.iso")
    
    # Generate audio
    subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "sine=frequency=1000:duration=5", str(media_dir / "test.mp3")], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "sine=frequency=1000:duration=5", "-c:a", "libopus", str(media_dir / "test.opus")], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if __name__ == "__main__":
    main()
