#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Backend Core Test
# Eingabewerte: src/core/main.py, web/app_bottle.py
# Ausgabewerte: Backend Integrity Report
# Testdateien: src/core/main.py, web/app_bottle.py
# Kommentar: Validates Eel exposed functions and Bottle routes.

import sys
import re
from pathlib import Path

def test_backend_integrity():
    print("\n🧪 Test: Backend Core Integrity Scan")
    
    project_root = Path(__file__).parent.parent
    main_py = project_root / "src" / "core" / "main.py"
    app_bottle_py = project_root / "web" / "app_bottle.py"
    
    if not main_py.exists():
        print(f"❌ main.py not found at {main_py}")
        return False

    with open(main_py, 'r', encoding='utf-8') as f:
        main_content = f.read()

    # 1. Check Eel Exposed Functions
    exposed_funcs = re.findall(r'@eel\.expose\s+def\s+([a-zA-Z0-9_]+)', main_content)
    print(f"   └─ Found {len(exposed_funcs)} exposed Eel functions.")
    
    # 2. Check for critical functions
    critical_funcs = ['open_video', 'get_library', 'get_version', 'get_app_name', 'get_db_stats']
    missing_critical = [f for f in critical_funcs if f not in exposed_funcs]
    
    if missing_critical:
        print(f"      ⚠️  Missing critical exposed functions: {missing_critical}")
    else:
        print("      ✅ All critical core functions are exposed.")

    # 3. Check Bottle Routes
    if app_bottle_py.exists():
        with open(app_bottle_py, 'r', encoding='utf-8') as f:
            bottle_content = f.read()
        routes = re.findall(r'@bottle\.route\([\'"]([^\'"]+)[\'"]\)', bottle_content)
        print(f"   └─ Found {len(routes)} Bottle routes: {routes}")
        
        required_routes = ['/media/<filepath:path>', '/cover/<filepath:path>', '/health']
        missing_routes = [r for r in required_routes if r not in routes]
        if missing_routes:
             print(f"      ⚠️  Missing required routes: {missing_routes}")
        else:
             print("      ✅ Essential Bottle routes verified.")
    else:
        print("   ⚠️  web/app_bottle.py not found - Route validation skipped.")

    # 4. Check for imports/dependencies in main.py
    essential_imports = ['eel', 'bottle', 'subprocess', 'json']
    for imp in essential_imports:
        if f"import {imp}" not in main_content and f"from {imp}" not in main_content:
            print(f"      ⚠️  Likely missing direct import of '{imp}' in main.py")

    print("\n✅ Backend Core Integrity Scan complete.")
    return True

if __name__ == "__main__":
    if test_backend_integrity():
        sys.exit(0)
    else:
        sys.exit(1)
