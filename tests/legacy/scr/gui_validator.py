#!/usr/bin/env python3
import sys
import re

def validate_gui_file(filepath, trace=False):
    print(f"--- Auditing {filepath} ---")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    div_stack = [] 
    brace_depth = 0
    script_mode = False
    style_mode = False
    js_template_mode = False
    
    errors = []
    
    # Matches: backtick, open/close script/style, open/close div, curly braces, comments, newline.
    # Order matters: check for backtick first inside script mode.
    pattern = re.compile(r'(`|<\/?script.*?>|<\/?style.*?>|<\/?div.*?>|[{}]|<!--.*?-->|\n)', re.DOTALL | re.IGNORECASE)
    
    line_num = 1
    pos = 0
    
    for match in pattern.finditer(content):
        before_match = content[pos:match.start()]
        line_num += before_match.count('\n')
        pos = match.end()
        
        token = match.group(0)
        token_lower = token.lower()
        
        if token == '\n':
            line_num += 1
            continue

        # Mode Toggles
        if token_lower.startswith('<script'):
            script_mode = True
            continue
        if token_lower == '</script>':
            script_mode = False
            js_template_mode = False
            continue
        if token_lower.startswith('<style'):
            style_mode = True
            continue
        if token_lower == '</style>':
            style_mode = False
            continue

        # JS Backtick Toggle
        if script_mode and token == '`':
            js_template_mode = not js_template_mode
            continue

        # If we are in a mode to be skipped, skip everything except the closing tags/backticks
        if js_template_mode or style_mode:
            continue
        
        # If in script mode (but not template), only track braces
        if script_mode:
            if token == '{':
                brace_depth += 1
            elif token == '}':
                brace_depth -= 1
                if brace_depth < 0:
                    errors.append(f"Line {line_num}: Negative JS BRACE depth ({brace_depth})")
                    brace_depth = 0
            continue

        # HTML Comments
        if token.startswith('<!--'):
            continue

        # Tag Tracking
        if token_lower.startswith('<div'):
            id_match = re.search(r'id=["\']([^"\']+)["\']', token, re.IGNORECASE)
            class_match = re.search(r'class=["\']([^"\']+)["\']', token, re.IGNORECASE)
            label = "div"
            if id_match: label += f'#{id_match.group(1)}'
            elif class_match: label += f'.{class_match.group(1).split()[0]}'
            
            div_stack.append((line_num, label))
            if trace: print(f"{line_num:5} | {'  '*len(div_stack)} OPEN {label}")
            
        elif token_lower == '</div>':
            if div_stack:
                ln, label = div_stack.pop()
                if trace: print(f"{line_num:5} | {'  '*len(div_stack)} CLOSE {label} (from line {ln})")
            else:
                ctx_start = max(0, match.start()-40)
                ctx_end = min(len(content), match.end()+40)
                context = content[ctx_start:ctx_end].replace('\n', ' ')
                errors.append(f"Line {line_num}: EXTRA </div> detected | ...{context}...")

        # Braces outside scripts/styles (likely CSS or rare inline HTML)
        elif token == '{':
            brace_depth += 1
        elif token == '}':
            brace_depth -= 1
            if brace_depth < 0:
                errors.append(f"Line {line_num}: Negative HTML/CSS BRACE depth ({brace_depth})")
                brace_depth = 0

    print(f"\nAudit Complete.")
    print(f"Final DIV stack size: {len(div_stack)}")
    print(f"Final BRACE depth: {brace_depth}")
    
    if div_stack:
        print("\n--- UNCLOSED TAGS ---")
        for ln, label in div_stack:
            print(f"Line {ln}: {label}")
            
    if errors:
        print("\n--- IDENTIFIED ISSUES ---")
        for err in errors:
            print(err)
    else:
        if not div_stack and brace_depth == 0:
            print("\nSUCCESS: No structural imbalances detected.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 gui_validator.py <path_to_html> [--trace]")
    else:
        do_trace = "--trace" in sys.argv
        validate_gui_file(sys.argv[1], trace=do_trace)
