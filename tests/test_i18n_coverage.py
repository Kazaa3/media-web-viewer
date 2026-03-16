#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: i18n Coverage Test
# Eingabewerte: web/app.html
# Ausgabewerte: Warning about potentially hardcoded strings in HTML
# Testdateien: web/app.html
# Kommentar: Scans HTML for text content that lacks data-i18n or t() wrapper.

import sys
import re
from pathlib import Path

def check_i18n_coverage():
    """Scan app.html for potentially hardcoded strings."""
    print("\n🧪 Test: i18n Coverage Scan")
    print("   └─ Searching for text content outside i18n wrappers")
    
    app_html = Path(__file__).parent.parent / "web" / "app.html"
    if not app_html.exists():
        print("❌ app.html not found")
        return False
        
    with open(app_html, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove script and style blocks for cleaner scanning
    content = re.sub(r'<script.*?>.*?</script>', '', content, flags=re.DOTALL)
    content = re.sub(r'<style.*?>.*?</style>', '', content, flags=re.DOTALL)
    
    # Find text between tags: >Text<
    # Exclude tags that usually don't contain i18n (like icons, spacers) or already have data-i18n
    # This is a heuristic approach.
    potential_strings = re.findall(r'>\s*([A-Z][^<>]{2,})\s*<', content)
    
    findings = []
    for s in potential_strings:
        s = s.strip()
        # Filter out common UI tokens, icons, or already handled ones
        if not s or s in ['&times;', '×', '▶', '⏸', '⛶', '⏪', '⏩', '⏱️', '🎚️', '🔀', '🔁']:
            continue
        if re.match(r'^[0-9\s.:,%/-]+$', s): # Numbers/Dates
            continue
        if len(s) < 3:
            continue
            
        # Check if the surrounding context (in the original content) has data-i18n
        # We search for the string in the original content to see its context
        # This is a bit slow but effective for a static check
        context_pattern = re.compile(r'<[^>]*data-i18n=[^>]*>\s*' + re.escape(s) + r'\s*<', re.DOTALL)
        if not context_pattern.search(content):
            findings.append(s)
            
    if findings:
        print(f"⚠️  Found {len(set(findings))} potentially hardcoded strings (missing data-i18n):")
        for f in sorted(list(set(findings))):
            print(f"   - {f}")
        return False
        
    print("✅ No obvious hardcoded strings found in HTML.")
    return True

if __name__ == "__main__":
    if check_i18n_coverage():
        sys.exit(0)
    else:
        sys.exit(0)
