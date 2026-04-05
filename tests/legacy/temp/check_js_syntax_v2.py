import re

def check_js_syntax(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Extract script blocks
    scripts = re.findall(r'<script.*?>\s*(.*?)\s*</script>', content, re.DOTALL)
    
    errors = []
    for script in scripts:
        # Check for unescaped double quotes inside attributes of strings (Heuristic)
        # Look for showToast("...width="12"..."
        matches = re.finditer(r'showToast\("(.*?)width="(.*?)"', script)
        for m in matches:
            errors.append(f"Potential nested quotes in showToast: {m.group(0)}")
            
        # Check for unbalanced parens in single lines (excluding multi-line blocks)
        lines = script.splitlines()
        for i, line in enumerate(lines, 1):
            if '(' in line or ')' in line:
                if line.count('(') != line.count(')'):
                    # Filter out common multi-line pattern: func(args) {
                    if not line.strip().endswith('{') and not line.strip().endswith('('):
                        if 'eel.' in line or 'showToast' in line:
                            errors.append(f"Unbalanced parens at line {i}: {line.strip()}")
    
    return errors

if __name__ == "__main__":
    errs = check_js_syntax('web/app.html')
    if errs:
        for e in errs:
            print(e)
    else:
        print("No obvious heuristics triggered.")
