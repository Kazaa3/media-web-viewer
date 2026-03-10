import subprocess

def test_python_vlc_import():
    """Test if python-vlc is installed and MediaPlayer is available."""
    try:
        import vlc
        assert hasattr(vlc, "MediaPlayer")
    except ImportError:
        assert False, "python-vlc nicht installiert"

def test_vlc_binary_available():
    """Test if VLC binary is available in the system."""
    result = subprocess.run(["which", "vlc"], capture_output=True, text=True)
    assert result.returncode == 0, "VLC-Binary nicht gefunden"

def test_vlc_version():
    """Test if VLC binary returns version info."""
    result = subprocess.run(["vlc", "--version"], capture_output=True, text=True)
    assert "VLC" in result.stdout