#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: UI / i18n Stability
# Eingabewerte: web/app.html (applyTranslations, package-count, requirements-count)
# Ausgabewerte: Verifiziert dass i18n-Translation dynamische Elemente nicht zerstört
# Testdateien: web/app.html, web/i18n.json
# Kommentar: Regression test for bug where applyTranslations() innerHTML destroys child elements

import unittest
from pathlib import Path
import re

class TestI18nPreservesDynamicElements(unittest.TestCase):
    """
    Test suite ensuring i18n translation system preserves dynamic DOM elements.
    
    Background:
    The applyTranslations() function uses el.innerHTML to replace translated text.
    This caused a critical bug where dynamic elements (package-count, requirements-count)
    were destroyed during translation, breaking the packages display.
    
    Solution:
    Move data-i18n attribute to a child <span>, so only the text span gets its innerHTML
    replaced, while sibling dynamic elements remain intact.
    """

    def setUp(self):
        """Initialize test environment with paths."""
        self.root = Path(__file__).parents[3]
        self.app_html = self.root / "web" / "app.html"
        self.html_code = self.app_html.read_text(encoding="utf-8")

    def test_01_package_count_not_inside_i18n_element(self):
        """Test: package-count element is not a child of element with data-i18n."""
        # Find the section with package-count
        package_section = re.search(
            r'<!-- Installed Packages.*?</div>.*?</div>',
            self.html_code,
            re.DOTALL
        )
        self.assertIsNotNone(package_section, "Should find Installed Packages section")
        section = package_section.group(0)
        
        # Verify package-count exists
        self.assertIn('id="package-count"', section)
        
        # Check structure: should NOT have pattern where package-count is inside data-i18n element
        # BAD pattern: <h4 data-i18n="...">....<span id="package-count">...
        # GOOD pattern: <h4><span data-i18n="...">...</span><span id="package-count">...
        
        # Extract the h4 element containing package-count
        h4_match = re.search(
            r'<h4[^>]*>.*?id="package-count".*?</h4>',
            section,
            re.DOTALL
        )
        self.assertIsNotNone(h4_match, "Should find h4 with package-count")
        h4_content = h4_match.group(0)
        
        # Method 1: Check if data-i18n is on h4 tag itself (BAD)
        h4_tag_match = re.match(r'<h4([^>]*)>', h4_content)
        self.assertIsNotNone(h4_tag_match)
        h4_attrs = h4_tag_match.group(1)
        self.assertNotIn('data-i18n=', h4_attrs, 
                        "h4 tag should NOT have data-i18n attribute (should be on child span)")
        
        # Method 2: Verify data-i18n is on a separate span before package-count
        # Structure should be: <h4><span data-i18n>text</span><span id="package-count">
        has_i18n_span = re.search(
            r'<h4[^>]*>\s*<span[^>]*data-i18n[^>]*>.*?</span>.*?<span\s+id="package-count"',
            h4_content,
            re.DOTALL
        )
        self.assertIsNotNone(has_i18n_span, 
                            "Should have structure: <h4><span data-i18n>text</span><span id='package-count'>...")

    def test_02_requirements_count_not_inside_i18n_element(self):
        """Test: requirements-count element is not a child of element with data-i18n."""
        # Find the section with requirements-count
        req_section = re.search(
            r'<!-- requirements\.txt Status.*?</div>.*?</div>',
            self.html_code,
            re.DOTALL
        )
        self.assertIsNotNone(req_section, "Should find requirements status section")
        section = req_section.group(0)
        
        # Verify requirements-count exists
        self.assertIn('id="requirements-count"', section)
        
        # Extract the h4 element containing requirements-count
        h4_match = re.search(
            r'<h4[^>]*>.*?id="requirements-count".*?</h4>',
            section,
            re.DOTALL
        )
        self.assertIsNotNone(h4_match, "Should find h4 with requirements-count")
        h4_content = h4_match.group(0)
        
        # Check if data-i18n is on h4 tag itself (BAD)
        h4_tag_match = re.match(r'<h4([^>]*)>', h4_content)
        self.assertIsNotNone(h4_tag_match)
        h4_attrs = h4_tag_match.group(1)
        self.assertNotIn('data-i18n=', h4_attrs,
                        "h4 tag should NOT have data-i18n attribute (should be on child span)")
        
        # Verify data-i18n is on a separate span before requirements-count
        has_i18n_span = re.search(
            r'<h4[^>]*>\s*<span[^>]*data-i18n[^>]*>.*?</span>.*?<span\s+id="requirements-count"',
            h4_content,
            re.DOTALL
        )
        self.assertIsNotNone(has_i18n_span,
                            "Should have structure: <h4><span data-i18n>text</span><span id='requirements-count'>...")

    def test_03_package_source_preserved(self):
        """Test: package-source element is preserved alongside package-count."""
        package_section = re.search(
            r'<!-- Installed Packages.*?</div>.*?</div>',
            self.html_code,
            re.DOTALL
        )
        self.assertIsNotNone(package_section)
        section = package_section.group(0)
        
        # Both elements should exist
        self.assertIn('id="package-count"', section)
        self.assertIn('id="package-source"', section)
        
        # Both should be siblings (not nested in data-i18n element)
        h4_match = re.search(
            r'<h4[^>]*>.*?id="package-count".*?id="package-source".*?</h4>',
            section,
            re.DOTALL
        )
        self.assertIsNotNone(h4_match, "Both package-count and package-source should be in h4")

    def test_04_apply_translations_uses_innerhtml(self):
        """Test: Verify applyTranslations function uses innerHTML (documenting the constraint)."""
        # This test documents the behavior that necessitates our fix
        apply_trans_match = re.search(
            r'function\s+applyTranslations\s*\([^)]*\)',
            self.html_code
        )
        self.assertIsNotNone(apply_trans_match, "Should find applyTranslations function")
        
        # Find the function body (approximate)
        func_start = apply_trans_match.end()
        func_end = self.html_code.find('function', func_start + 100)  # Find next function
        if func_end == -1:
            func_end = func_start + 2000
        func_body = self.html_code[func_start:func_end]
        
        # Verify it uses innerHTML
        self.assertIn('innerHTML', func_body, 
                     "applyTranslations uses innerHTML, which is why we need the nested span structure")
        
        # Verify it handles data-i18n attribute
        self.assertIn('data-i18n', func_body)

    def test_05_regression_test_structure_example(self):
        """Test: Document the correct structure pattern for future reference."""
        # This is a documentation test showing the correct pattern
        
        # WRONG (causes bug):
        # <h4 data-i18n="key">Translated Text <span id="dynamic">value</span></h4>
        # → applyTranslations will do: h4.innerHTML = "Translated Text"
        # → Result: <span id="dynamic"> is destroyed!
        
        # CORRECT (bug-free):
        # <h4><span data-i18n="key">Translated Text</span> <span id="dynamic">value</span></h4>
        # → applyTranslations will do: span.innerHTML = "Translated Text"
        # → Result: sibling <span id="dynamic"> remains intact!
        
        # Verify our fixed elements have the correct structure
        correct_patterns = [
            (r'<h4[^>]*>\s*<span[^>]*data-i18n="options_installed_packages"[^>]*>.*?</span>.*?<span\s+id="package-count"', 
             "options_installed_packages section"),
            (r'<h4[^>]*>\s*<span[^>]*data-i18n="options_requirements_status"[^>]*>.*?</span>.*?<span\s+id="requirements-count"',
             "options_requirements_status section"),
        ]
        
        for pattern, description in correct_patterns:
            match = re.search(pattern, self.html_code, re.DOTALL)
            self.assertIsNotNone(match, f"Should have correct nested structure in {description}")

    def test_06_all_critical_dynamic_elements_exist(self):
        """Test: All critical dynamic elements that could be destroyed by i18n exist in HTML."""
        critical_ids = [
            'package-count',
            'package-source',
            'requirements-count',
            'requirements-last-checked',
            'requirements-status-list',
            'installed-packages-list'
        ]
        
        for element_id in critical_ids:
            self.assertIn(f'id="{element_id}"', self.html_code,
                         f"Element with id='{element_id}' should exist in HTML")

    def test_08_no_data_i18n_on_container_with_dynamic_children(self):
        """Test: Critical package/requirements elements don't have data-i18n on parent."""
        # Focus only on the critical elements that broke package display
        critical_elements = [
            ('package-count', 'options_installed_packages'),
            ('package-source', 'options_installed_packages'),
            ('requirements-count', 'options_requirements_status'),
        ]
        
        for element_id, related_i18n_key in critical_elements:
            # Find the element
            element_match = re.search(
                rf'id="{element_id}"',
                self.html_code
            )
            self.assertIsNotNone(element_match, f"Element {element_id} should exist")
            
            # Find the containing h4 or div
            # Search backwards and forwards from the element to find its parent
            start = max(0, element_match.start() - 500)
            end = min(len(self.html_code), element_match.end() + 500)
            context = self.html_code[start:end]
            
            # Check that the parent tag doesn't have data-i18n with the related key
            # Pattern: <h4 ... data-i18n="key" ...> ... id="element_id"
            bad_pattern = rf'<(h\d|div)[^>]*data-i18n="{related_i18n_key}"[^>]*>[^<]*<[^>]*id="{element_id}"'
            has_bad_pattern = re.search(bad_pattern, context, re.DOTALL)
            
            self.assertIsNone(has_bad_pattern,
                f"Element {element_id} should NOT be a direct child of element with data-i18n='{related_i18n_key}'. "
                f"Use nested <span data-i18n> structure instead.")

if __name__ == "__main__":
    unittest.main()
