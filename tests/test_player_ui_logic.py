import unittest
from pathlib import Path

class TestPlayerUILogic(unittest.TestCase):
    def setUp(self):
        self.app_html_path = Path(__file__).parent.parent / "web" / "app.html"
        with open(self.app_html_path, "r", encoding="utf-8") as f:
            self.content = f.read()

    def test_shuffle_button_exists(self):
        self.assertIn('id="btn-shuffle"', self.content)
        self.assertIn('onclick="toggleShuffle()"', self.content)

    def test_repeat_button_exists(self):
        self.assertIn('id="btn-repeat"', self.content)
        self.assertIn('onclick="toggleRepeat()"', self.content)

    def test_navigation_buttons_exist(self):
        self.assertIn('onclick="playPrev()"', self.content)
        self.assertIn('onclick="playNext()"', self.content)

    def test_playlist_tab_exists(self):
        self.assertIn('onclick="switchTab(\'playlist\'', self.content)
        self.assertIn('id="playlist-tab"', self.content)
        self.assertIn('id="playlist-list"', self.content)

    def test_js_functions_implemented(self):
        self.assertIn('function toggleShuffle()', self.content)
        self.assertIn('function toggleRepeat()', self.content)
        self.assertIn('function playNext()', self.content)
        self.assertIn('function playPrev()', self.content)
        self.assertIn('function renderPlaylist()', self.content)

    def test_autoplay_listener_exists(self):
        self.assertIn('currentPlayer.onended', self.content)

if __name__ == "__main__":
    unittest.main()
