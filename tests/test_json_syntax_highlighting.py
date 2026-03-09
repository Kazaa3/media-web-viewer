#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: UI Frontend Test
# Eingabewerte: JSON data for syntax highlighting
# Ausgabewerte: HTML with colored syntax elements
# Testdateien: web/app.html
# Kommentar: Testet JSON Syntax-Highlighting im Python Dict (Details) Element.
"""
Test Suite for JSON Syntax Highlighting in Debug Tab

Tests the "Python Dict (Details)" element which displays JSON data
with syntax highlighting in VS Code Dark+ theme colors.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""

import unittest
import sys
import re
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestJsonSyntaxHighlighting(unittest.TestCase):
    """Test JSON syntax highlighting functionality in Debug tab."""
    
    def setUp(self):
        """Load app.html content for testing."""
        self.app_html_path = Path(__file__).parent.parent / "web" / "app.html"
        with open(self.app_html_path, 'r', encoding='utf-8') as f:
            self.html_content = f.read()
    
    def test_debug_items_json_element_exists(self):
        """Test that debug-items-json element exists in HTML."""
        self.assertIn('id="debug-items-json"', self.html_content)
        print("✓ debug-items-json element found in HTML")
    
    def test_debug_items_dict_container_exists(self):
        """Test that debug-items-dict-container wrapper exists."""
        self.assertIn('id="debug-items-dict-container"', self.html_content)
        print("✓ debug-items-dict-container element found in HTML")
    
    def test_syntax_highlight_function_exists(self):
        """Test that syntaxHighlight function is defined."""
        self.assertIn('function syntaxHighlight', self.html_content)
        print("✓ syntaxHighlight function is defined")
    
    def test_syntax_highlight_function_has_color_definitions(self):
        """Test that syntaxHighlight function contains VS Code color palette."""
        # Check for key colors from VS Code Dark+ theme
        colors = {
            '#9cdcfe': 'Keys (bright blue)',
            '#ce9178': 'Strings (orange)',
            '#b5cea8': 'Numbers (soft green)',
            '#569cd6': 'Booleans/Null (blue)'
        }
        
        for color, description in colors.items():
            self.assertIn(color, self.html_content,
                         f"Color {color} for {description} not found")
            print(f"✓ Color {color} for {description} found")
    
    def test_dark_theme_background(self):
        """Test that dark theme background is applied."""
        # Check for dark background color
        self.assertIn('#1e1e1e', self.html_content)
        print("✓ Dark theme background (#1e1e1e) applied")
    
    def test_gradient_border_styling(self):
        """Test that gradient border is applied to container."""
        # Check for gradient styling
        pattern = r'linear-gradient\(135deg,\s*#667eea\s+0%,\s*#764ba2\s+100%\)'
        self.assertRegex(self.html_content, pattern)
        print("✓ Gradient border styling found")
    
    def test_fira_code_font_family(self):
        """Test that Fira Code monospace font is used."""
        pattern = r"font-family:\s*['\"]Fira Code"
        self.assertRegex(self.html_content, pattern)
        print("✓ Fira Code font family specified")
    
    def test_syntax_highlight_is_called(self):
        """Test that syntaxHighlight function is actually invoked."""
        # Check if syntaxHighlight is called with result.media
        pattern = r'syntaxHighlight\s*\(\s*result\.media\s*\)'
        self.assertRegex(self.html_content, pattern)
        print("✓ syntaxHighlight function is called with result.media")
    
    def test_html_injection_via_innerHTML(self):
        """Test that highlighted JSON is injected via innerHTML."""
        pattern = r'debugItemsJson\.innerHTML\s*=\s*highlighted'
        self.assertRegex(self.html_content, pattern)
        print("✓ Highlighted JSON is injected via innerHTML")
    
    def test_regex_pattern_for_json_elements(self):
        """Test that the regex pattern matches JSON elements correctly."""
        # Extract the regex pattern from syntaxHighlight function
        pattern_match = re.search(
            r'json\.replace\(/(.+?)/g,\s*function',
            self.html_content
        )
        self.assertIsNotNone(pattern_match, "JSON regex pattern not found")
        
        regex_pattern = pattern_match.group(1)
        
        # Verify it captures the essential JSON elements
        required_patterns = [
            'true|false|null',  # Booleans and null literals
            r'-?\d+',  # Numbers (integers and floats)
        ]
        
        for req_pattern in required_patterns:
            self.assertRegex(regex_pattern, req_pattern,
                         f"Pattern {req_pattern} not found in regex")
        
        # Also check that string quotes are handled
        self.assertIn('"', regex_pattern, "String quote handling not found")
        
        print("✓ JSON regex pattern contains all required matchers")
    
    def test_python_dict_section_title(self):
        """Test that 'Python Dict (Details)' title is present."""
        self.assertIn('Python Dict (Details)', self.html_content)
        print("✓ Section title 'Python Dict (Details)' found")
    
    def test_section_description(self):
        """Test that description text is present."""
        pattern = r'Item-Dictionary.*Python-Backend'
        self.assertRegex(self.html_content, pattern, 
                        "Section description not found")
        print("✓ Section description text found")
    
    def test_html_escaping_in_syntax_highlight(self):
        """Test that syntaxHighlight function escapes HTML entities."""
        # Check for HTML entity escaping
        escaping_patterns = [
            r'\.replace\(/&/g,\s*[\'"]&amp;',
            r'\.replace\(/</g,\s*[\'"]&lt;',
            r'\.replace\(/>/g,\s*[\'"]&gt;'
        ]
        
        for pattern in escaping_patterns:
            self.assertRegex(self.html_content, pattern,
                           f"HTML escaping pattern {pattern} not found")
        
        print("✓ HTML entity escaping is implemented")
    
    def test_json_key_highlighting_with_weight(self):
        """Test that JSON keys are highlighted with font-weight: 500."""
        pattern = r'font-weight:\s*500'
        self.assertRegex(self.html_content, pattern)
        print("✓ JSON keys have font-weight: 500 for emphasis")
    
    def test_loading_state_placeholder(self):
        """Test that 'Loading data...' placeholder exists."""
        # Check for i18n key or direct text
        loading_patterns = [
            'debug_loading_data',
            'Lade Daten',
            'Loading data'
        ]
        
        found = any(p in self.html_content for p in loading_patterns)
        self.assertTrue(found, "Loading placeholder not found")
        print("✓ Loading state placeholder found")


class TestSyntaxHighlightLogic(unittest.TestCase):
    """Test the logic of syntax highlighting with simulated JavaScript behavior."""
    
    def test_color_assignments_are_correct(self):
        """Verify color assignments match VS Code Dark+ theme."""
        app_html_path = Path(__file__).parent.parent / "web" / "app.html"
        with open(app_html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Simply check if colors appear in the HTML content after syntaxHighlight is defined
        # This is more reliable than trying to extract the function body
        syntax_start = content.find('function syntaxHighlight')
        self.assertNotEqual(syntax_start, -1, "syntaxHighlight function not found")
        
        # Get section from syntaxHighlight to the next major function
        syntax_section = content[syntax_start:syntax_start + 2000]  # 2000 chars should cover it
        
        # Verify color mappings
        color_checks = [
            ('#9cdcfe', 'json-key', 'Keys'),
            ('#ce9178', 'json-string', 'Strings'),
            ('#b5cea8', 'json-number', 'Numbers'),
            ('#569cd6', 'json-boolean', 'Booleans'),
        ]
        
        for color, cls, name in color_checks:
            self.assertIn(color, syntax_section, f"Color {color} for {name} not found")
            self.assertIn(cls, syntax_section, f"Class {cls} for {name} not found")
            print(f"✓ {name} correctly mapped to {color} (class: {cls})")


if __name__ == '__main__':
    print("=" * 70)
    print("JSON Syntax Highlighting Test Suite")
    print("Testing 'Python Dict (Details)' element in Debug Tab")
    print("=" * 70)
    unittest.main(verbosity=2)
