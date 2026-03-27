"""
Installed Tools & Version Unit Test (DE/EN)

DE:
Testet, ob wichtige Programme installiert sind und die Version korrekt ausgelesen wird.
EN:
Tests if essential programs are installed and their version is correctly detected.

Usage:
    pytest tests/test_installed_tools_version.py
"""

import pytest
import subprocess

TOOLS = [
    ("python", "Python"),
    ("ffmpeg", "ffmpeg"),
    ("ffprobe", "ffprobe"),
    ("vlc", "VLC"),
    ("pip", "pip"),
    ("mkvinfo", "mkvinfo"),
    ("mkvmerge", "mkvmerge"),
    ("chromium-browser", "Chromium"),
    ("chrome", "Chrome"),
    ("google-chrome", "Chrome"),
    ("firefox", "Firefox"),
    ("firefox-developer-edition", "Firefox Developer"),
]

# CLI tool support test candidates (Browsers & Video Engines)
#
# This list includes all major Linux CLI-capable browsers and video engines.
# Each entry is checked for installation and version via '--version'.
#
# - chromium-browser: Chromium
# - chrome: Chrome
# - google-chrome: Chrome
# - firefox: Firefox
# - firefox-developer-edition: Firefox Developer
# - vlc: VLC
VIDEO_ENGINES = [
    ("chromium-browser", "Chromium"),
    ("chrome", "Chrome"),
    ("google-chrome", "Chrome"),
    ("firefox", "Firefox"),
    ("firefox-developer-edition", "Firefox Developer"),
    ("vlc", "VLC"),
]

# --- Test Classification & Project Management ---
#
# Test Classes:
# - TestInstalledToolsVersion: Validates installation and version detection for essential CLI tools and video engines.
#
# Test Types:
# - Environment/Dependency Validation: Ensures all required tools are present and functional.
# - Media Engine Support: Confirms browser/video engine candidates are available for playback.
#
# Project Management Notes:
# - Keep tool lists up-to-date with new media engines and browsers.
# - Document all test candidates and their CLI invocation method.
# - Use parameterized tests for extensibility and maintainability.
# - Integrate results into milestone documentation and environment validation reports.
# - Review and refactor test classes as new requirements emerge.
#
# For further details, see docs/TEST_SUITE_SUMMARY.md and docs/Project_Markdown_File_List.md.

class TestInstalledToolsVersion:
    @pytest.mark.parametrize("tool, expected", TOOLS)
    def test_tool_installed_and_version(self, tool, expected):
        """
        DE:
        Prüft, ob das Tool installiert ist und die Version ausgelesen werden kann.
        EN:
        Checks if the tool is installed and its version can be detected.
        """
        try:
            result = subprocess.run([tool, "--version"], capture_output=True, text=True)
            assert result.returncode == 0
            output = result.stdout + result.stderr
            assert expected.lower() in output.lower()
        except FileNotFoundError:
            pytest.skip(f"{tool} not installed.")

    @pytest.mark.parametrize("engine, expected", VIDEO_ENGINES)
    def test_video_engine_installed(self, engine, expected):
        """
        DE:
        Prüft, ob der Video-Engine-Kandidat installiert ist.
        EN:
        Checks if the video engine candidate is installed.
        """
        try:
            result = subprocess.run([engine, "--version"], capture_output=True, text=True)
            assert result.returncode == 0
            output = result.stdout + result.stderr
            assert expected.lower() in output.lower()
        except FileNotFoundError:
            pytest.skip(f"{engine} not installed.")
