import re
from pathlib import Path

def run_diagnostics():
    app_html = Path("web/app.html")
    if not app_html.exists():
        print("❌ app.html not found!")
        return

    content = app_html.read_text(encoding='utf-8')
    print(f"File: {app_html} ({len(content)} bytes)")

    # Level 1: Structural Balance (Robust)
    print("\n[L1] Structural Balance:")
    open_divs = len(re.findall(r"<div", content))
    close_divs = len(re.findall(r"</div", content))
    
    brace_open = 0
    brace_close = 0
    i = 0
    n = len(content)
    while i < n:
        if content[i:i+2] == '//':
            i = content.find('\n', i)
            if i == -1: break
        elif content[i:i+2] == '/*':
            i = content.find('*/', i)
            if i == -1: break
            i += 2
        elif content[i] in "'\"`":
            quote = content[i]
            i += 1
            while i < n:
                if content[i] == '\\': i += 2
                elif content[i] == quote:
                    i += 1
                    break
                else: i += 1
        elif content[i] == '{':
            brace_open += 1
            i += 1
        elif content[i] == '}':
            brace_close += 1
            i += 1
        else:
            i += 1
    
    print(f"  DIVs: {open_divs}/{close_divs} {'✅' if open_divs == close_divs else '❌'}")
    print(f"  Braces: {brace_open}/{brace_close} {'✅' if brace_open == brace_close else '❌'}")

    # Level 2: CSS Tokens (Updated)
    print("\n[L2] CSS Token Audit:")
    required_vars = ["--bg-main", "--accent-color", "--text-main", "--sidebar-width"]
    for v in required_vars:
        found = v in content
        print(f"  {v}: {'✅' if found else '❌'}")

    # Level 3: Critical IDs (Updated)
    print("\n[L3] Critical Selectors:")
    required_ids = ["main-sidebar", "main-content-area", "player-controls", "library-tab"]
    for rid in required_ids:
        found = f'id="{rid}"' in content or f"id='{rid}'" in content
        print(f"  #{rid}: {'✅' if found else '❌'}")

    # Level 10: Debug & DB
    print("\n[L10] Debug & DB View:")
    required_ids = ["debug-flag-persistence-panel", "debug-db-info", "lib-db-table-body", "debug-items-json"]
    for rid in required_ids:
        found = f'id="{rid}"' in content
        print(f"  #{rid}: {'✅' if found else '❌'}")

    # Level 12: Mock System
    print("\n[L12] Mock System:")
    has_toggle = 'id="config-mock-data-toggle"' in content
    has_logic = "async function toggleMockData" in content
    print(f"  Toggle: {'✅' if has_toggle else '❌'}")
    print(f"  Logic: {'✅' if has_logic else '❌'}")

if __name__ == "__main__":
    run_diagnostics()
