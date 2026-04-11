import pytest
from unittest.mock import patch
from pathlib import Path
from src.core.main import open_video_smart, PLAYBACK_LOCKS

@pytest.fixture
def mock_backend():
    with patch("src.core.main.resolve_media_path", side_effect=lambda x: x), \
         patch("src.core.main.is_mkvtoolnix_available", return_value=True), \
         patch("src.core.main.db.get_media_by_path", return_value={"id": 123}):
        yield

@pytest.fixture
def clean_locks():
    PLAYBACK_LOCKS.clear()
    yield
    PLAYBACK_LOCKS.clear()

def test_mp4_h264_direct_play(mock_backend, clean_locks):
    """Verifies that standard MP4 (H264) uses Chrome Direct Play."""
    test_path = "/media/perfect_movie.mp4"
    meta = {"codec": "h264", "container": "mp4"}
    
    with patch("src.core.main.get_video_metadata", return_value=meta):
        res = open_video_smart(test_path, mode="auto")
        
        assert res["status"] == "play"
        assert res["mode"] == "chrome_direct"
        assert res["path"] == f"/media/{Path(test_path).name}"

def test_mkv_remux_priority(mock_backend, clean_locks):
    """Verifies that MKV files prioritize the MKVMerge PIPE-KIT (Remux)."""
    test_path = "/media/standard_movie.mkv"
    meta = {"codec": "h264", "container": "matroska"}
    
    with patch("src.core.main.get_video_metadata", return_value=meta):
        res = open_video_smart(test_path, mode="auto")
        
        assert res["status"] == "play"
        assert res["mode"] == "chrome_remux"
        assert res.get("path", "").startswith("/video-remux-stream/")

def test_mpeg2_vlc_fallback(mock_backend, clean_locks):
    """Verifies that legacy MPEG-2 (DVD PAL) forces VLC fallback."""
    test_path = "/media/abc.mkv"
    meta = {"codec": "mpeg2video", "container": "matroska"}
    
    with patch("src.core.main.get_video_metadata", return_value=meta), \
         patch("src.core.main.open_video", side_effect=lambda *args, **kwargs: {"status": "ok", "mode": "vlc_iso"}) as mock_open:
        
        res = open_video_smart(test_path, mode="auto")
        
        assert res["status"] == "ok"
        assert res["mode"] == "vlc_iso"
        # Must be called with VLC and the correct source
        assert mock_open.called
        assert mock_open.call_args[1].get('source') == "smart_router_mpeg_pal"

def test_dvd_folder_vlc_guard(mock_backend, clean_locks):
    """Verifies that DVD folders (4 Köpfe etc) force the guarded VLC instance."""
    test_dir = "/media/DVD_OBJECT"
    
    with patch("os.path.isdir", return_value=True), \
         patch("src.core.main.os.path.exists", side_effect=lambda p: True if "VIDEO_TS" in str(p) or str(p) == test_dir else False), \
         patch("src.core.main.os.listdir", return_value=["VIDEO_TS"]), \
         patch("src.core.main.get_video_metadata", return_value={}), \
         patch("src.core.main.open_video", side_effect=lambda *args, **kwargs: {"status": "ok", "mode": "vlc_iso"}) as mock_open:
        
        res = open_video_smart(test_dir, mode="auto")
        
        assert res["status"] == "ok"
        assert mock_open.called
        assert mock_open.call_args[1].get('source') == "smart_router_dvd"

def test_smart_router_hierarchy_logic(mock_backend, clean_locks):
    """Verifies the overall smart routing hierarchy: Native -> Remux -> FragMP4."""
    # Test unknown codec falls back to FragMP4
    test_path = "/media/odd_codec.mkv"
    meta = {"codec": "hevc", "container": "matroska"} # Assume HEVC not native in this test env
    
    with patch("src.core.main.get_video_metadata", return_value=meta):
        # We manually simulate is_mkvtoolnix_available = False for this one
        with patch("src.core.main.is_mkvtoolnix_available", return_value=False):
            res = open_video_smart(test_path, mode="auto")
            assert res["status"] == "play"
            assert res["mode"] == "chrome_fragmp4" # Standard FFmpeg fallback
