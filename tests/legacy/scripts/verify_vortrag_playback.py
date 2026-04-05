#!/usr/bin/env python3
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append("/home/xc/#Coding/gui_media_web_viewer")

from src.core.main import open_video

def test_routing():
    media_dir = Path("/home/xc/#Coding/gui_media_web_viewer/media")
    mock_dir = media_dir / "mock_files"
    
    # 1. Real "Vortrag" file
    vortrag_file = media_dir / "30. Pleisweiler Gespräch - Vortrag - Prof. Dr. Gertraud Teuchert-Noodt - 21. Oktober 2018 (720p_30fps_H264-192kbit_AAC).mp4"
    if vortrag_file.exists():
        res = open_video(str(vortrag_file))
        print(f"Vortrag Routing: {res}")
        assert res.get("mode") == "chrome_direct", f"Expected chrome_direct for Vortrag, got {res.get('mode')}"
    else:
        print("Vortrag file not found, skipping real file test.")

    # 2. MKV (should use remux)
    mkv_file = mock_dir / "test.mkv"
    if mkv_file.exists():
        res = open_video(str(mkv_file))
        print(f"MKV Routing: {res}")
        # Even if status is error (missing DB item), the mode should be chrome_remux
        assert res.get("mode") == "chrome_remux", f"Expected chrome_remux for MKV, got {res.get('mode')}"

    # 3. ISO (should use VLC)
    iso_file = mock_dir / "test_movie.iso"
    if iso_file.exists():
        res = open_video(str(iso_file))
        print(f"ISO Routing: {res}")
        assert res.get("mode") == "vlc_dvd", f"Expected vlc_dvd for ISO, got {res}"

    # 4. Audio
    audio_file = mock_dir / "test.mp3"
    if audio_file.exists():
        res = open_video(str(audio_file))
        print(f"Audio Routing: {res}")
        assert res.get("mode") == "chrome_direct", f"Expected chrome_direct for Audio (MP3), got {res.get('mode')}"

    print("✅ All routing tests passed!")

if __name__ == "__main__":
    try:
        test_routing()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)
