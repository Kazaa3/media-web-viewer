import os
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
from src.core.main import open_video_smart, PLAYBACK_LOCKS

@pytest.fixture
def mock_path_resolution():
    with patch("src.core.main.resolve_media_path", side_effect=lambda x: x):
        yield

@pytest.fixture
def clean_locks():
    PLAYBACK_LOCKS.clear()
    yield
    PLAYBACK_LOCKS.clear()

def test_iso_file_routing(mock_path_resolution, clean_locks):
    """Verifies that .iso files are forced to VLC via the smart router."""
    test_path = "/media/test_film.iso"
    
    with patch("src.core.main.get_video_metadata", return_value={"codec": "h264"}), \
         patch("src.core.main.open_video") as mock_open:
        
        mock_open.return_value = {"status": "ok", "mode": "vlc_iso"}
        
        res = open_video_smart(test_path, mode="auto")
        
        assert res["status"] == "ok"
        # Source must be smart_router_dvd (not auto)
        mock_open.assert_called_once_with(test_path, "vlc", "vlc_iso", source="smart_router_dvd")

def test_video_ts_folder_routing(mock_path_resolution, clean_locks):
    """Verifies that folders containing VIDEO_TS are forced to VLC."""
    test_dir = "/media/DVD_FOLDER"
    
    with patch("src.core.main.os.path.isdir", return_value=True), \
         patch("src.core.main.os.path.exists", side_effect=lambda p: True if "VIDEO_TS" in str(p) or str(p) == test_dir else False), \
         patch("src.core.main.os.listdir", return_value=["VIDEO_TS"]), \
         patch("src.core.main.get_video_metadata", return_value={}), \
         patch("src.core.main.open_video") as mock_open:
        
        mock_open.return_value = {"status": "ok", "mode": "vlc_iso"}
        
        res = open_video_smart(test_dir, mode="auto")
        
        assert res["status"] == "ok"
        mock_open.assert_called_once_with(test_dir, "vlc", "vlc_iso", source="smart_router_dvd")

def test_mpeg2_pal_fallback(mock_path_resolution, clean_locks):
    """Verifies that MPEG-2 (DVD PAL) MKVs are forced to VLC even if they aren't ISOs."""
    test_path = "/media/abc.mkv"
    
    # Simulate MPEG-2 detection
    with patch("src.core.main.get_video_metadata", return_value={"codec": "mpeg2video"}), \
         patch("src.core.main.open_video") as mock_open:
        
        mock_open.return_value = {"status": "ok", "mode": "vlc_iso"}
        
        res = open_video_smart(test_path, mode="auto")
        
        assert res["status"] == "ok"
        # Source must be smart_router_mpeg_pal
        mock_open.assert_called_once_with(test_path, "vlc", "vlc_iso", source="smart_router_mpeg_pal")

def test_debouncing_lock(mock_path_resolution, clean_locks):
    """Verifies that rapid duplicate calls are blocked by the 2.0s lock."""
    test_path = "/media/movie.mp4"
    
    with patch("src.core.main.get_video_metadata", return_value={"codec": "h264"}), \
         patch("src.core.main.open_video") as mock_open:
        
        mock_open.return_value = {"status": "ok"}
        
        # First call: Proceed
        res1 = open_video_smart(test_path, mode="auto")
        assert res1["status"] == "ok"
        
        # Second call (immediate): Blocked
        res2 = open_video_smart(test_path, mode="auto")
        assert res2["status"] == "error"
        assert res2["error"] == "Debounced"
        
        assert mock_open.call_count == 1
