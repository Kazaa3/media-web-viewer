#!/usr/bin/env python3
import sys
import re

def validate_gui_file(filepath, trace=False):
    print(f"--- Auditing {filepath} ---")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    div_stack = [] 
    brace_depth = 0
    script_mode = False
    style_mode = False
    
    errors = []

    for i, line in enumerate(lines, 1):
        line_clean = line.strip()
        
        # Detect block transitions
        if '<script' in line.lower(): script_mode = True
        if '</script>' in line.lower(): script_mode = False
        if '<style' in line.lower(): style_mode = True
        if '</style>' in line.lower(): style_mode = False
        
        # Tag tracking (Ignore inside script/style)
        if not script_mode and not style_mode:
            # Find opens like <div id="foo" class="bar">
            opens = re.findall(r'<div([^>]*?)>', line, re.IGNORECASE)
            for attr_str in opens:
                # Try to find ID or Class for context
                id_match = re.search(r'id=["\']([^"\']+)["\']', attr_str)
                class_match = re.search(r'class=["\']([^"\']+)["\']', attr_str)
                label = "div"
                if id_match: label += f'#{id_match.group(1)}'
                elif class_match: label += f'.{class_match.group(1).split()[0]}'
                div_stack.append((i, label))
                if trace: print(f"{i:5} | {'  '*len(div_stack)} OPEN {label}")
                
            # Find closes </div>
            closes = re.findall(r'</div', line, re.IGNORECASE)
            for _ in closes:
                if div_stack:
                    ln, label = div_stack.pop()
                    if trace: print(f"{i:5} | {'  '*len(div_stack)} CLOSE {label} (from line {ln})")
                else:
                    errors.append(f"Line {i}: EXTRA </div> detected (orphaned) | {line_clean[:60]}...")

        # Brace tracking (mainly for CSS and JS)
        brace_opens = line.count('{')
        brace_closes = line.count('}')
        
        brace_depth += brace_opens
        brace_depth -= brace_closes
        
        if brace_depth < 0:
            errors.append(f"Line {i}: Negative BRACE depth ({brace_depth}) | {line_clean[:60]}...")
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
