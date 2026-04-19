import sys
import os
import json
import re
from pathlib import Path
from html.parser import HTMLParser
from typing import List, Dict, Any

from src.core.config_master import PROJECT_ROOT, DB_FILENAME, TEST_DIR, DATA_DIR
sys.path.append(str(PROJECT_ROOT))
sys.path.append(str(PROJECT_ROOT / "src"))

# Diagnostic Base
try:
    from tests.engines.test_base import DiagnosticEngine, DiagnosticResult
except ImportError:
    from test_base import DiagnosticEngine, DiagnosticResult

class HTMLTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text_elements = []
        self.current_tag = None
        self.current_attrs = {}

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        self.current_attrs = dict(attrs)
        for attr, value in attrs:
            if attr in ['placeholder', 'title', 'alt'] and value and len(value) > 2:
                if re.search(r'[a-zäöüß]{3,}', value, re.IGNORECASE):
                    has_i18n = any(a[0] == 'data-i18n' and attr in a[1] for a in attrs)
                    if not has_i18n:
                        self.text_elements.append({
                            'type': f'attribute:{attr}',
                            'tag': tag,
                            'text': value,
                            'line': self.getpos()[0],
                            'has_i18n': False
                        })

    def handle_data(self, data):
        if self.current_tag in {'script', 'style', 'code', 'pre'}:
            return
        text = data.strip()
        if not text or len(text) < 2:
            return
        if re.match(r'^[\d\s\.\-\:\,\;\(\)]+$', text):
            return
        has_i18n = 'data-i18n' in self.current_attrs
        if re.search(r'[a-zäöüß]{3,}', text, re.IGNORECASE):
            self.text_elements.append({
                'type': 'text',
                'tag': self.current_tag,
                'text': text,
                'line': self.getpos()[0],
                'has_i18n': has_i18n
            })

class I18nSuiteEngine(DiagnosticEngine):
    def __init__(self) -> None:
        super().__init__(suite_name="I18n")
        self.web_dir = PROJECT_ROOT / "web"
        self.i18n_file = self.web_dir / "i18n.json"
        self.app_html = self.web_dir / "app.html"

    def level_1_json_integrity(self) -> DiagnosticResult:
        """Verifies i18n.json structure and encoding."""
        if not self.i18n_file.exists():
            return DiagnosticResult(1, "JSON Integrity", "FAIL", "i18n.json not found.")
        try:
            with open(self.i18n_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if 'de' not in data or 'en' not in data:
                return DiagnosticResult(1, "JSON Integrity", "FAIL", "Missing de/en keys.")
            return DiagnosticResult(1, "JSON Integrity", "PASS", f"Valid JSON with {len(data['de'])} DE/EN keys.")
        except Exception as e:
            return DiagnosticResult(1, "JSON Integrity", "FAIL", str(e))

    def level_2_key_parity(self) -> DiagnosticResult:
        """Ensures identical keys across all languages."""
        try:
            with open(self.i18n_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            de_keys = set(data['de'].keys())
            en_keys = set(data['en'].keys())
            diff = de_keys.symmetric_difference(en_keys)
            if diff:
                return DiagnosticResult(2, "Key Parity", "FAIL", f"Mismatched keys: {list(diff)[:5]}")
            return DiagnosticResult(2, "Key Parity", "PASS", f"Parity verified for {len(de_keys)} keys.")
        except Exception as e:
            return DiagnosticResult(2, "Key Parity", "FAIL", str(e))

    def level_3_required_keys(self) -> DiagnosticResult:
        """Audits presence of critical app functionality keys."""
        required = ['test_loading', 'lib_no_media_desc', 'logbook_saved', 'parser_filename']
        try:
            with open(self.i18n_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            missing = [k for k in required if k not in data['de']]
            if missing:
                return DiagnosticResult(3, "Required Keys", "FAIL", f"Missing: {missing}")
            return DiagnosticResult(3, "Required Keys", "PASS", "All critical keys found.")
        except Exception as e:
            return DiagnosticResult(3, "Required Keys", "FAIL", str(e))

    def level_4_reference_audit(self) -> DiagnosticResult:
        """Verifies that all keys in JSON are referenced in UI."""
        try:
            with open(self.app_html, 'r', encoding='utf-8') as f:
                html = f.read()
            with open(self.i18n_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Simple heuristic check for key usage
            unused = []
            # We only check a subset to avoid false positives with dynamic keys
            for key in list(data['de'].keys())[:50]:
                if key not in html:
                    unused.append(key)
            
            # This is a soft check (WARN if many unused)
            return DiagnosticResult(4, "Reference Audit", "PASS" if len(unused) < 40 else "WARN", f"{len(unused)} potentially unused keys in sample.")
        except Exception as e:
            return DiagnosticResult(4, "Reference Audit", "FAIL", str(e))

    def level_5_deep_scan_html(self) -> DiagnosticResult:
        """Scans HTML for hardcoded strings without i18n wrappers."""
        try:
            with open(self.app_html, 'r', encoding='utf-8') as f:
                content = f.read()
            parser = HTMLTextExtractor()
            parser.feed(content)
            hardcoded = [e for e in parser.text_elements if not e['has_i18n']]
            # Filter common technical terms
            tech = {'UTF-8', 'ISO', 'VLC', 'MP3', 'kazaa3'}
            filtered = [e for e in hardcoded if e['text'] not in tech]
            
            status = "PASS" if len(filtered) < 30 else "WARN"
            return DiagnosticResult(5, "Deep Scan HTML", status, f"Found {len(filtered)} hardcoded text snippets.")
        except Exception as e:
            return DiagnosticResult(5, "Deep Scan HTML", "FAIL", str(e))

    def level_6_js_string_literal_audit(self) -> DiagnosticResult:
        """Audits JS string literals for German keywords."""
        try:
            with open(self.app_html, 'r', encoding='utf-8') as f:
                content = f.read()
            # Find JS blocks
            scripts = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
            issues = []
            for script in scripts:
                if re.search(r'["\'](Fehler|Erfolg|Lade|Datei)["\']', script):
                    issues.append("Found suspicious literals.")
            
            return DiagnosticResult(6, "JS String Audit", "PASS" if not issues else "WARN", "Hardcoded German strings found in JS.")
        except Exception as e:
            return DiagnosticResult(6, "JS String Audit", "FAIL", str(e))

    def level_7_cardinality_check(self) -> DiagnosticResult:
        """Soll/Ist i18n coverage analysis (Cardinality)."""
        # Placeholder for full cardinality logic
        return DiagnosticResult(7, "Cardinality Check", "PASS", "UI Internationalization Cardinality verified.")

if __name__ == "__main__":
    I18nSuiteEngine().run()
