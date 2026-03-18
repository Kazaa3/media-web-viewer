import pytest
from unittest.mock import patch, MagicMock
import os
import time
from src.core.main import open_video_smart, ACTIVE_SUBPROCESSES, PLAYBACK_LOCKS

@pytest.fixture(autouse=True)
def clean_locks():
    """Cleans all playback locks before each test."""
    PLAYBACK_LOCKS.clear()
    yield
    PLAYBACK_LOCKS.clear()

@pytest.fixture
def mock_dvd_env():
    """Mocks a generic DVD directory environment for testing."""
    dvd_path = "/home/xc/#Coding/gui_media_web_viewer/media/Test DVD (2015) - DVD"
    video_ts = os.path.join(dvd_path, "VIDEO_TS")

    with patch("os.path.isdir", return_value=True), \
         patch("os.path.exists", side_effect=lambda p: True if str(p) in [dvd_path, video_ts] else False), \
         patch("os.listdir", return_value=["VIDEO_TS"]), \
         patch("src.core.main.resolve_media_path", return_value=dvd_path), \
         patch("shutil.which", return_value="/usr/bin/vlc"), \
         patch("subprocess.Popen") as mock_popen:

        # Mock Popen to return a mock process
        mock_proc = MagicMock()
        mock_popen.return_value = mock_proc
        yield dvd_path, mock_popen

def test_dvd_iso_embedded_routing(mock_dvd_env):
    """Verifies that a generic DVD ISO is correctly routed to the HLS Embedded Streamer."""
    path, mock_popen = mock_dvd_env

    # Trigger smart routing for the DVD path
    res = open_video_smart(path, mode="auto")

    # Assertions
    assert res["status"] == "play"
    assert res["mode"] == "vlc_embedded"
    assert res["path"] == "/vlc-hls-live/stream.m3u8"
    assert res["type"] == "application/x-mpegURL"

    # Verify subprocess call
    args, kwargs = mock_popen.call_args
    cmd_list = args[0]

    assert "/usr/bin/vlc" in cmd_list
    assert f"dvd://{path}" in cmd_list

    # Verify HLS sout parameters
    sout_val = ""
    for i, arg in enumerate(cmd_list):
        if arg == "--sout":
            sout_val = cmd_list[i+1]
            break
    assert "livehttp" in sout_val
    assert "index=/tmp/vlc_hls/stream.m3u8" in sout_val