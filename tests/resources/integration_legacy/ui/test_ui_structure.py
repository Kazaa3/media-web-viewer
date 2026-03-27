import os
import re
import unittest

class TestUIStructure(unittest.TestCase):
    """
    Test suite to verify the HTML structure of app.html.
    Checks for tag consistency (especially <div>), tab IDs, and footer position.
    """

    def setUp(self):
        # Determine the root directory (where web/ is located)
        # tests/integration/ui/test_ui_structure.py -> 3 levels up to root
        self.root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
        self.app_path = os.path.join(self.root_dir, "web/app.html")
        
        with open(self.app_path, 'r', encoding='utf-8') as f:
            self.content = f.read()

    def test_div_balance(self):
        """Verify that opening and closing <div> tags are balanced."""
        open_divs = len(re.findall(r'<div\b', self.content))
        close_divs = len(re.findall(r'</div\b', self.content))
        
        self.assertEqual(open_divs, close_divs, 
                         f"Unbalanced <div> tags: Found {open_divs} opening and {close_divs} closing tags.")

    def test_tab_ids_consistency(self):
        """Verify that all tabs mentioned in navigation buttons exist as div IDs (or in tabMap)."""
        # Extract the tabMap from the JS
        tab_map_match = re.search(r'const tabMap = \{([\s\S]+?)\};', self.content)
        self.assertIsNotNone(tab_map_match, "Could not find tabMap in app.html")
        
        tab_map_content = tab_map_match.group(1)
        # Parse simple 'key': 'value' entries
        tab_map = {}
        for line in tab_map_content.split('\n'):
            m = re.search(r"['\"]([^'\"]+)['\"]\s*:\s*['\"]([^'\"]+)['\"]", line)
            if m:
                tab_map[m.group(1)] = m.group(2)
        
        # Find all switchTab('tab-id', ...) calls in the whole file
        tab_calls = re.findall(r"switchTab\(['\"]([^'\"]+)['\"]", self.content)
        unique_tabs = set(tab_calls)
        
        for tab_id in unique_tabs:
            if tab_id.startswith('$'): continue # Skip template literals
            
            target_id = tab_map.get(tab_id, tab_id)
            self.assertIn(f'id="{target_id}"', self.content, 
                          f"Navigation tab '{tab_id}' (maps to '{target_id}') has no corresponding element with that ID.")

    def test_footer_position(self):
        """Verify the footer (player-container) is not nested inside the main layout-container."""
        layout_container_start = self.content.find('id="main-split-container"')
        footer_start = self.content.find('class="player-container"')
        
        self.assertNotEqual(layout_container_start, -1, "Could not find layout-container")
        self.assertNotEqual(footer_start, -1, "Could not find player-container (footer)")
        
        # Structure trace: look for all divs between layout start and footer.
        layout_chunk = self.content[layout_container_start:footer_start]
        open_count = len(re.findall(r'<div\b', layout_chunk))
        close_count = len(re.findall(r'</div\b', layout_chunk))
        
        # If footer is outside, we must have closed as many divs as we opened 
        # (including the layout-container itself).
        self.assertEqual(open_count, close_count, 
                         f"Footer (player-container) appears to be nested! "
                         f"Between layout start and footer, {open_count} divs were opened but only {close_count} closed.")

if __name__ == '__main__':
    unittest.main()
