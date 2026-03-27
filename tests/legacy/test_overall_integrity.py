
import os
import sys
import ast
import time
from pathlib import Path

def check_python_integrity(root_dir):
    """Checks all Python files in the given directory for syntax errors."""
    findings = []
    py_files = list(Path(root_dir).rglob("*.py"))
    print(f"Analyzing {len(py_files)} Python files for SyntaxErrors...")
    
    for py_file in py_files:
        if ".venv" in str(py_file) or "__pycache__" in str(py_file):
            continue
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
                ast.parse(content)
        except SyntaxError as e:
            msg = f"SyntaxError in {py_file.relative_to(root_dir)} at line {e.lineno}: {e.msg}"
            findings.append(msg)
        except Exception as e:
            # Skip files that might be binary or locked
            pass
            
    return findings

def check_html_div_balance(html_path):
    """Checks the div tag balance of a single HTML file."""
    findings = []
    if not html_path.exists():
        return [f"File not found: {html_path}"]
    
    print(f"Analyzing HTML balance for {html_path.name}...")
    try:
        content = html_path.read_text(encoding='utf-8')
        opens = content.count("<div")
        closes = content.count("</div")
        
        if opens != closes:
            findings.append(f"Div imbalance detected: {opens} opens vs {closes} closes.")
        else:
            print(f"  -> ✅ Tags balanced ({opens} pairs).")
    except Exception as e:
        findings.append(f"Error reading HTML: {e}")
        
    return findings

def run_suite():
    print("--- OVERALL INTEGRITY TEST SUITE ---")
    print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    project_root = Path(__file__).parents[1]
    src_dir = project_root / "src"
    web_dir = project_root / "web"
    app_html = web_dir / "app.html"
    
    # 1. Python Integrity
    py_findings = check_python_integrity(src_dir)
    
    # 2. HTML Integrity
    html_findings = check_html_div_balance(app_html)
    
    print("\n--- Summary ---")
    success = True
    
    if py_findings:
        print("[FAIL] Python Syntax Errors found:")
        for f in py_findings:
            print(f"  - {f}")
        success = False
    else:
        print("[PASS] Python syntax is clean.")
        
    if html_findings:
        print("[FAIL] HTML Integrity issues found:")
        for f in html_findings:
            print(f"  - {f}")
        success = False
    else:
        print("[PASS] HTML structure is balanced.")
        
    return success

if __name__ == "__main__":
    if run_suite():
        sys.exit(0)
    else:
        sys.exit(1)
