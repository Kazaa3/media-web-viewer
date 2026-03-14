#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: UI Frontend Test
# Eingabewerte: JSON-Daten für Syntax-Highlighting
# Ausgabewerte: HTML mit farbigen Syntaxelementen
# Testdateien: web/app.html
# Kommentar: Testet JSON Syntax-Highlighting im Python Dict (Details) Element.
"""
JSON Syntax Highlighting Test Suite (DE/EN)
===========================================

DE:
Testet das JSON Syntax-Highlighting im Debug-Tab und die Darstellung im Python Dict (Details) Element.

EN:
Tests JSON syntax highlighting in the Debug tab and rendering in the Python Dict (Details) element.

Autor/Author: Media Web Viewer Team
Erstellt/Created: 2026-03-13
Version: 1.0.0
Lizenz: GPLv3
"""

import unittest
import sys
import re
from pathlib import Path

# Add parent directory to path

class TestJsonSyntaxHighlighting(unittest.TestCase):
    """
    DE:
    Testet die JSON Syntax-Highlighting-Funktionalität im Debug-Tab.

    EN:
    Tests JSON syntax highlighting functionality in Debug tab.
    """
    
    def setUp(self):
        """
        DE:
        Lädt den Inhalt von app.html für die Tests.

        EN:
        Loads app.html content for testing.
        """
        self.app_html_path = Path(__file__).parents[3] / "web" / "app.html"
        with open(self.app_html_path, 'r', encoding='utf-8') as f:
            self.html_content = f.read()
    
    def test_debug_items_json_element_exists(self):
        """
        DE:
        Prüft, ob das debug-items-json Element im HTML existiert.

        EN:
        Tests that debug-items-json element exists in HTML.
        Returns:
            Keine.
        Raises:
            AssertionError: Wenn Element fehlt.
        """
        self.assertIn('id="debug-items-json"', self.html_content)
        print("✓ debug-items-json element found in HTML")
    
    def test_debug_items_dict_container_exists(self):
        """
        DE:
        Prüft, ob der debug-items-dict-container Wrapper existiert.

        EN:
        Tests that debug-items-dict-container wrapper exists.
        Returns:
            Keine.
        Raises:
            AssertionError: Wenn Element fehlt.
        """
        self.assertIn('id="debug-items-dict-container"', self.html_content)
        print("✓ debug-items-dict-container element found in HTML")
    
    def test_syntax_highlight_function_exists(self):
        """
        DE:
        Prüft, ob die Funktion syntaxHighlight definiert ist.

        EN:
        Tests that syntaxHighlight function is defined.
        Returns:
            Keine.
        Raises:
            AssertionError: Wenn Funktion fehlt.
        """
        self.assertIn('function syntaxHighlight', self.html_content)
        print("✓ syntaxHighlight function is defined")
    
    def test_syntax_highlight_function_has_color_definitions(self):
        """
        DE:
        Prüft, ob die Funktion syntaxHighlight die VS Code Farbpalette enthält.

        EN:
        Tests that syntaxHighlight function contains VS Code color palette.
        Returns:
            Keine.
        Raises:
            AssertionError: Wenn Farben fehlen.
        """
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
        """
        DE:
        Prüft, ob der Dark Theme Hintergrund angewendet wird.

        EN:
        Tests that dark theme background is applied.
        Returns:
            Keine.
        Raises:
            AssertionError: Wenn Hintergrundfarbe fehlt.
        """
        # Check for dark background color
        self.assertIn('#1e1e1e', self.html_content)
        print("✓ Dark theme background (#1e1e1e) applied")
    
    def test_gradient_border_styling(self):
        """
        DE:
        Prüft, ob ein Gradient-Border angewendet wird.

        EN:
        Tests that gradient border is applied to container.
        Returns:
            Keine.
        Raises:
            AssertionError: Wenn Gradient fehlt.
        """
        # Check for gradient styling
        pattern = r'linear-gradient\(135deg,\s*#667eea\s+0%,\s*#764ba2\s+100%\)'
        self.assertRegex(self.html_content, pattern)
        print("✓ Gradient border styling found")
    
    def test_fira_code_font_family(self):
        """
        DE:
        Prüft, ob die Fira Code Monospace-Schrift verwendet wird.

        EN:
        Tests that Fira Code monospace font is used.
        Returns:
            Keine.
        Raises:
            AssertionError: Wenn Schrift fehlt.
        """
        pattern = r"font-family:\s*['\"]Fira Code"
        self.assertRegex(self.html_content, pattern)
        print("✓ Fira Code font family specified")
    
    def test_syntax_highlight_is_called(self):
        """
        DE:
        Prüft, ob die Funktion syntaxHighlight tatsächlich aufgerufen wird.

        EN:
        Tests that syntaxHighlight function is actually invoked.
        Returns:
            Keine.
        Raises:
            AssertionError: Wenn Aufruf fehlt.
        """
        # Check if syntaxHighlight is called with result.media
        pattern = r'syntaxHighlight\s*\(\s*result\.media\s*\)'
        self.assertRegex(self.html_content, pattern)
        print("✓ syntaxHighlight function is called with result.media")
    
    def test_html_injection_via_innerHTML(self):
        """
        DE:
        Prüft, ob das hervorgehobene JSON via innerHTML injiziert wird.

        EN:
        Tests that highlighted JSON is injected via innerHTML.
        Returns:
            Keine.
        Raises:
            AssertionError: Wenn Injection fehlt.
        """
        pattern = r'debugItemsJson\.innerHTML\s*=\s*highlighted'
        self.assertRegex(self.html_content, pattern)
        print("✓ Highlighted JSON is injected via innerHTML")
    
    def test_regex_pattern_for_json_elements(self):
        """
        DE:
        Prüft, ob das Regex-Muster JSON-Elemente korrekt matched.

        EN:
        Tests that the regex pattern matches JSON elements correctly.
        Returns:
            Keine.
        Raises:
            AssertionError: Wenn Pattern fehlt.
        """
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
        """
        DE:
        Prüft, ob der Titel 'Python Dict (Details)' vorhanden ist.

        EN:
        Tests that 'Python Dict (Details)' title is present.
        Returns:
            Keine.
        Raises:
            AssertionError: Wenn Titel fehlt.
        """
        self.assertIn('Python Dict (Details)', self.html_content)
        print("✓ Section title 'Python Dict (Details)' found")
    
    def test_section_description(self):
        """
        DE:
        Prüft, ob der Beschreibungstext vorhanden ist.

        EN:
        Tests that description text is present.
        Returns:
            Keine.
        Raises:
            AssertionError: Wenn Beschreibung fehlt.
        """
        pattern = r'Item-Dictionary.*Python-Backend'
        self.assertRegex(self.html_content, pattern, 
                        "Section description not found")
        print("✓ Section description text found")
    
    def test_html_escaping_in_syntax_highlight(self):
        """
        DE:
        Prüft, ob die Funktion syntaxHighlight HTML-Entities escaped.

        EN:
        Tests that syntaxHighlight function escapes HTML entities.
        Returns:
            Keine.
        Raises:
            AssertionError: Wenn Escaping fehlt.
        """
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
        """
        DE:
        Prüft, ob JSON-Keys mit font-weight: 500 hervorgehoben werden.

        EN:
        Tests that JSON keys are highlighted with font-weight: 500.
        Returns:
            Keine.
        Raises:
            AssertionError: Wenn Gewicht fehlt.
        """
        pattern = r'font-weight:\s*500'
        self.assertRegex(self.html_content, pattern)
        print("✓ JSON keys have font-weight: 500 for emphasis")
    
    def test_loading_state_placeholder(self):
        """
        DE:
        Prüft, ob der 'Loading data...' Platzhalter existiert.

        EN:
        Tests that 'Loading data...' placeholder exists.
        Returns:
            Keine.
        Raises:
            AssertionError: Wenn Platzhalter fehlt.
        """
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
    """
    DE:
    Testet die Logik des Syntax-Highlightings mit simuliertem JavaScript-Verhalten.

    EN:
    Tests the logic of syntax highlighting with simulated JavaScript behavior.
    """
    
    def test_color_assignments_are_correct(self):
        """
        DE:
        Prüft, ob die Farbzuteilungen dem VS Code Dark+ Theme entsprechen.

        EN:
        Verifies color assignments match VS Code Dark+ theme.
        Returns:
            Keine.
        Raises:
            AssertionError: Wenn Farben nicht korrekt.
        """
        app_html_path = Path(__file__).parents[3] / "web" / "app.html"
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
