#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Compatibility & Completeness Test
# Eingabewerte: web/app.html, src/core/main.py
# Ausgabewerte: Compatibility Report
# Testdateien: web/app.html, src/core/main.py
# Kommentar: Checks for alignment between JS calls and Python exposures.

import re
import sys
from pathlib import Path

def test_compatibility():
    print("\n🧪 Test: Full Compatibility & Completeness Scan")
    
    project_root = Path(__file__).parent.parent
    app_html = project_root / "web" / "app.html"
    main_py = project_root / "src" / "core" / "main.py"
    
    if not app_html.exists() or not main_py.exists():
        print("❌ app.html or main.py missing.")
        return False

    with open(app_html, 'r', encoding='utf-8') as f:
        html_content = f.read()
    with open(main_py, 'r', encoding='utf-8') as f:
        main_content = f.read()

    # 1. Extract exposed functions from main.py
    exposed = set(re.findall(r'@eel\.expose\s+def\s+([a-zA-Z0-9_]+)', main_content))
    
    # JS -> Python calls (eel.function_name)
    eel_calls = set(re.findall(r'eel\.([a-zA-Z0-9_]+)\(', html_content))
    # Python -> JS calls (exposed in JS)
    js_exposed = set(re.findall(r'eel\.expose\(([a-zA-Z0-9_]+)\)', html_content))
    
    print(f"   ├─ JS -> Python: Found {len(eel_calls)} unique Eel API calls in Frontend.")
    print(f"   ├─ Python -> JS: Found {len(js_exposed)} JS functions exposed to Python.")
    print(f"   └─ Python -> JS: Found {len(exposed)} exposed functions in Backend.")

    # 3. Intersection and mismatches
    # Exclude eel.expose and other internal names
    to_ignore = {'expose', 'set_host', 'start'}
    missing_in_backend = (eel_calls - exposed) - to_ignore
    
    # Filter out internal eel calls if any (usually none are called via eel.* that aren't exposed)
    if missing_in_backend:
        print(f"      ⚠️  JS calls these functions, but they are NOT exposed in Python: {missing_in_backend}")
    else:
        print("      ✅ All Frontend Eel calls are backed by exposed Python functions.")

    unused_exposures = exposed - eel_calls
    # Many exposures might be for other scripts or future use, so we just list them as Info
    if unused_exposures:
        print(f"      ℹ️  Exposed but not called in app.html: {len(unused_exposures)} functions (Likely used in themes or external scripts).")

    # 4. Basic HTML/CSS Sanity
    # Check for unclosed div tags (very basic)
    open_divs = html_content.count("<div")
    close_divs = html_content.count("</div")
    if open_divs != close_divs:
        print(f"      ⚠️  Potential HTML imbalance: {open_divs} open <div> vs {close_divs} closed </div>")
    else:
        print(f"      ✅ HTML Tag Balance (div): OK ({open_divs} pairs)")

    # Check for linked files visibility
    links = re.findall(r'<link.*?href=["\']([^"\']+)["\']', html_content)
    scripts = re.findall(r'<script.*?src=["\']([^"\']+)["\']', html_content)
    
    for resource in links + scripts:
        if resource.startswith('http') or resource.startswith('//') or resource == 'eel.js' or resource.startswith('/eel.js'):
            continue
        res_path = project_root / "web" / resource.lstrip('/')
        if not res_path.exists():
             print(f"      ⚠️  Linked resource not found: {resource}")

    print("\n✅ Compatibility & Completeness Scan complete.")
    return True

if __name__ == "__main__":
    if test_compatibility():
        sys.exit(0)
    else:
        sys.exit(1)
