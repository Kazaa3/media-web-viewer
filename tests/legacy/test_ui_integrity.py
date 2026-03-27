#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: UI Integrity Test
# Eingabewerte: web/app.html
# Ausgabewerte: UI structure validation
# Testdateien: web/app.html
# Kommentar: Testet UI-Integrität.
import unittest
import re
from pathlib import Path
import sys
import os

class TestUIIntegrity(unittest.TestCase):
    """
    @brief Structural integrity tests for app.html.
    @details Validates the HTML structure and JS configuration to prevent UI regressions.
    """

    def setUp(self):
        self.root = Path(__file__).parent.parent
        self.app_html_path = self.root / "web" / "app.html"
        with open(self.app_html_path, 'r', encoding='utf-8') as f:
            self.content = f.read()

    def test_div_tag_balance(self):
        """
        @test Verify that opening and closing <div> tags are balanced.
        @details Automated structural check for app.html to prevent "layout ghosting"
                 by counting and validating the balance of div opening and closing tags.
        """
        # Using regex to find <div> tags (including those with attributes)
        opens = len(re.findall(r'<div\b', self.content, re.IGNORECASE))
        closes = len(re.findall(r'</div\b', self.content, re.IGNORECASE))
        self.assertEqual(opens, closes, f"Unbalanced <div> tags: {opens} open vs {closes} close")

    def test_critical_tab_ids(self):
        """
        @test Ensure all required tab containers exist in the DOM.
        @details Checks for the presence of all required tab IDs (video-tab, 
                 logbuch-tab, etc.) to ensure the UI structure is complete.
        """
        required_ids = [
            "active-queue-tab-trigger", 
            "coverflow-library-tab-trigger", 
            "filesystem-crawler-tab-trigger", 
            "system-registry-tab-trigger", 
            "app-footer",
            "sync-indicator",
            "main-split-container",
            "qa-validation-tab-trigger", 
            "documentation-journal-tab-trigger",
            "media-orchestrator-tab-trigger"
        ]
        for rid in required_ids:
            # Look for id="rid"
            pattern = f'id="{rid}"'
            self.assertIn(pattern, self.content, f"Critical Tab ID '{rid}' not found in app.html")

    def test_tab_map_completeness(self):
        """
        @test Verify that the tabMap JS object contains all necessary keys.
        @details Parses the tabMap JS object and verifies it contains all necessary 
                 keys (logbuch, vlc, video) for consistent navigation.
        """
        # Extract the tabMap block
        match = re.search(r'const tabMap = \{(.*?)\};', self.content, re.DOTALL)
        self.assertTrue(match, "tabMap definition not found in switchTab function")
        
        tab_map_str = match.group(1)
        required_keys = ['player', 'library', 'item', 'file', 'edit', 'options', 'parser', 'debug', 'tests', 'logbuch', 'playlist', 'vlc']
        
        for key in required_keys:
            self.assertIn(f"'{key}'", tab_map_str, f"Key '{key}' missing from tabMap")

    def test_switch_tab_calls(self):
        """
        @test Verify that all switchTab calls in the HTML use known tab IDs.
        @details Checks that every switchTab call in the HTML corresponds to a 
                 valid entry in the tabMap, preventing navigation to missing tabs.
        """
        # Find all switchTab('id', ...) calls
        calls = re.findall(r"switchTab\('([^']+)'", self.content)
        
        # Extract keys from tabMap to validate against
        match = re.search(r'const tabMap = \{(.*?)\};', self.content, re.DOTALL)
        tab_map_str = match.group(1)
        valid_keys = re.findall(r"'([^']+)'\s*:", tab_map_str)
        
        for call_id in calls:
            if call_id.startswith("${"):
                continue
            self.assertIn(call_id, valid_keys, f"switchTab called with unknown ID '{call_id}'")

    def test_sync_indicator_elements(self):
        """
        @test Verify that the sync indicator elements exist.
        @details Checks for sync-indicator, sync-dot, and sync-text IDs.
        """
        for sid in ["sync-indicator", "sync-dot", "sync-text"]:
            self.assertIn(f'id="{sid}"', self.content, f"Sync indicator ID '{sid}' missing")

    def test_sidebar_split_ids(self):
        """Ensure splitter and sidebar IDs used in JS exist in HTML."""
        required_ids = ["main-sidebar", "main-splitter", "main-split-container"]
        for rid in required_ids:
            self.assertIn(f'id="{rid}"', self.content, f"Layout ID '{rid}' missing")

    def test_no_duplicate_js_functions(self):
        """
        @test Verify no JS function is defined more than once in app.html.
        @details Duplicate function definitions (e.g. seekVideo, toggleSpeed, togglePip)
                 cause SyntaxErrors like 'unexpected token'. This regression check
                 detects them statically.
        """
        # Extract named functions (function foo(...) and async function foo(...))
        func_defs = re.findall(
            r'\basync\s+function\s+(\w+)\s*\(|(?<!\w)function\s+(\w+)\s*\(',
            self.content
        )
        names = [a or b for a, b in func_defs]
        seen = {}
        duplicates = []
        for name in names:
            seen[name] = seen.get(name, 0) + 1
            if seen[name] == 2:
                duplicates.append(name)
        self.assertEqual(
            duplicates, [],
            f"Duplicate JS function definitions found: {duplicates}"
        )

    def test_no_orphaned_catch_blocks(self):
        """
        @test Verify no '} catch' block exists without a matching 'try {' above it.
        @details Uses a backwards scan from each '} catch' up to the nearest function
                 boundary to confirm there is an unmatched 'try {'. Handles long functions.
        """
        lines = self.content.split('\n')
        suspicious = []
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if not re.match(r'^\}\s*catch\s*[\(\{]', stripped):
                continue
            # Scan backwards to find the nearest function definition or file start
            catch_depth = 0
            found_try = False
            for j in range(i - 2, max(0, i - 600), -1):
                lj = lines[j].strip()
                if re.search(r'\btry\s*\{', lj):
                    if catch_depth == 0:
                        found_try = True
                        break
                    catch_depth -= 1
                elif re.match(r'^\}\s*catch\s*[\(\{]', lj):
                    catch_depth += 1
                # Stop at the enclosing function start
                if re.match(r'(async\s+)?function\s+\w+\s*\(', lj):
                    break
            if not found_try:
                suspicious.append(f"Line {i}: {stripped}")
        self.assertEqual(
            suspicious, [],
            f"Orphaned catch block(s) found:\n" + "\n".join(suspicious)
        )



if __name__ == '__main__':
    print("Running UI Integrity Tests...")
    unittest.main()
