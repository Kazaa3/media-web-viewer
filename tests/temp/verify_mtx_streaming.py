import os
import sys
from unittest.mock import MagicMock, patch

# Mock Eel and other dependencies before importing main
import types
eel = MagicMock()
eel.btl = MagicMock()
eel.expose = lambda x: x
sys.modules['eel'] = eel
sys.modules['bottle'] = MagicMock()
sys.modules['env_handler'] = MagicMock()

# Import the function to test
# We need to simulate the environment
with patch('src.core.main.resolve_media_path', side_effect=lambda x: x):
    from src.core.main import stream_to_mediamtx

def test_stream_to_mediamtx():
    print("--- Testing MediaMTX Stream Generation ---")
    
    # Mock os.path.exists and subprocess.Popen
    with patch('os.path.exists', return_value=True), \
         patch('subprocess.Popen') as mock_popen, \
         patch('time.sleep'):
        
        # 1. Test MKV (Remux)
        print("\n[Test 1] MKV File (Remuxing)")
        res = stream_to_mediamtx("movie.mkv", protocol="hls")
        print(f"Result: {res}")
        args = mock_popen.call_args[0][0]
        print(f"FFmpeg Cmd: {' '.join(args)}")
        assert "-c copy" in ' '.join(args)
        assert "rtsp://localhost:8554/movie" in ' '.join(args)

        # 2. Test M4V (Remux)
        print("\n[Test 2] M4V File (Remuxing)")
        res = stream_to_mediamtx("video.m4v", protocol="hls")
        print(f"Result: {res}")
        args = mock_popen.call_args[0][0]
        print(f"FFmpeg Cmd: {' '.join(args)}")
        assert "video.m4v" in ' '.join(args)

        # 3. Test DVD ISO (Transcode)
        print("\n[Test 3] DVD ISO (Transcoding)")
        # We need to ensure .iso triggers the DVD path
        res = stream_to_mediamtx("dvd.iso", protocol="webrtc")
        print(f"Result: {res}")
        args = mock_popen.call_args[0][0]
        print(f"FFmpeg Cmd: {' '.join(args)}")
        assert "-c:v libx264" in ' '.join(args)
        assert "protocol=webrtc" in str(res) or "mode=mediamtx_webrtc" in str(res)

    print("\n--- ALL TESTS PASSED ---")

if __name__ == "__main__":
    test_stream_to_mediamtx()
