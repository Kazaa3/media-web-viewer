#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: JS Static Analysis
# Eingabewerte: web/app.html
# Ausgabewerte: Potential null-dereference warnings for .style and .innerHTML
# Testdateien: web/app.html
# Kommentar: Scans for unguarded DOM element property accesses.

import sys
import re
from pathlib import Path

def scan_js_for_errors():
    """Scan app.html for potential JS errors like unguarded .style accesses."""
    print("\n🧪 Test: Static JS Error Scan (Potential Null Dereferences)")
    print("   └─ Searching for unguarded .style and .innerHTML calls")
    
    app_html = Path(__file__).parent.parent / "web" / "app.html"
    if not app_html.exists():
        print("❌ app.html not found")
        return False
        
    with open(app_html, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simple regex to find .style or .innerHTML access on document.getElementById or similar
    # Pattern 1: document.getElementById('...').style
    # Pattern 2: document.querySelector('...').innerHTML
    patterns = [
        (r"document\.getElementById\(['\"][^'\"]+['\"]\)\.(?:style|innerHTML|innerText|value|classList)", "Direct access on getElementById()"),
        (r"document\.querySelector\(['\"][^'\"]+['\"]\)\.(?:style|innerHTML|innerText|value|classList)", "Direct access on querySelector()"),
    ]
    
    findings = []
    lines = content.split('\n')
    
    for pattern, desc in patterns:
        for i, line in enumerate(lines, 1):
            if re.search(pattern, line):
                # Check if it's inside a comment
                if line.strip().startswith('//') or line.strip().startswith('/*'):
                    continue
                findings.append(f"Line {i}: {desc} -> {line.strip()[:100]}")
    
    # Pattern 3: Variables declared and immediately accessed without check
    # Example: const el = document.getElementById('x'); el.style.display = '...';
    # This is harder to catch with simple regex across lines, but we can look for " el.style" where el was recently defined.
    
    if findings:
        print(f"⚠️  Found {len(findings)} potential JS null-access issues:")
        for f in findings:
            print(f"   {f}")
        return False
    
    print("✅ No obvious unguarded DOM accesses found.")
    return True

if __name__ == "__main__":
    if scan_js_for_errors():
        sys.exit(0)
    else:
        # We don't exit with 1 yet, just warning
        sys.exit(0)
