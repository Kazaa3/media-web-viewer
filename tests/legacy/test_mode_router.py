import pytest
from unittest.mock import patch
from src.core.mode_router import smart_route

@pytest.fixture
def mock_analyzer():
    with patch('src.core.mode_router.ffprobe_analyze') as mock:
        yield mock

def test_direct_play_routing(mock_analyzer):
    """Test that H.264 MP4 triggers Direct Play."""
    mock_analyzer.return_value = {
        "codec": "h264",
        "container": "mp4",
        "resolution": "1080p",
        "is_iso": False,
        "has_menus": False,
        "atmos": False
    }
    assert smart_route("test.mp4") == "direct_play"

def test_4k_hls_routing(mock_analyzer):
    """Test that 4K content triggers HLS fMP4 (Universal)."""
    mock_analyzer.return_value = {
        "codec": "h264",
        "container": "mp4",
        "resolution": "4K",
        "is_iso": False,
        "has_menus": False,
        "atmos": False
    }
    assert smart_route("test_4k.mp4") == "hls_fmp4"

def test_iso_vlc_routing(mock_analyzer):
    """Test that ISO files trigger VLC Bridge."""
    mock_analyzer.return_value = {
        "codec": "mpeg2video",
        "container": "mpegts",
        "resolution": "SD",
        "is_iso": True,
        "has_menus": True,
        "atmos": False
    }
    assert smart_route("movie.iso") == "vlc_bridge"

def test_atmos_vlc_routing(mock_analyzer):
    """Test that Atmos content triggers VLC Bridge (for advanced audio)."""
    mock_analyzer.return_value = {
        "codec": "h264",
        "container": "mkv",
        "resolution": "1080p",
        "is_iso": False,
        "has_menus": False,
        "atmos": True
    }
    assert smart_route("atmos_demo.mkv") == "vlc_bridge"

def test_mkv_mse_routing(mock_analyzer):
    """Test that 1080p MKV triggers MSE (Low-Latency Transcode)."""
    mock_analyzer.return_value = {
        "codec": "hevc",
        "container": "matroska",
        "resolution": "1080p",
        "is_iso": False,
        "has_menus": False,
        "atmos": False
    }
    assert smart_route("movie.mkv") == "mse"

def test_fallback_routing(mock_analyzer):
    """Test that errors fallback to direct_play safely."""
    mock_analyzer.return_value = {"error": "ffprobe failed"}
    assert smart_route("corrupt.avi") == "direct_play"

if __name__ == "__main__":
    import sys
    sys.exit(pytest.main([__file__]))
