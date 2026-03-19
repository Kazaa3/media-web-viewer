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
    comment_mode = False
    
    errors = []

    for i, line in enumerate(lines, 1):
        line_clean = line.strip()
        
        # Refined segment parsing
        segments = re.split(r'(<[^>]+>)', line)
        for seg in segments:
            if not seg or not seg.strip(): continue
            seg_lower = seg.lower()
            if trace and i == 2677: print(f"DEBUG {i}: seg='{seg}' comment={comment_mode} script={script_mode}")
            
            if seg.startswith('<!--'): comment_mode = True
            if '-->' in seg: 
                comment_mode = False
                continue
            if comment_mode: continue

            if '<script' in seg_lower: script_mode = True
            if '</script' in seg_lower: 
                script_mode = False
                continue
            if '<style' in seg_lower: style_mode = True
            if '</style' in seg_lower: 
                style_mode = False
                continue

            if script_mode or style_mode: continue

            # Track DIVs (Open)
            opens = re.findall(r'<div([^>]*?)(?:>|$)', seg, re.IGNORECASE)
            for attr_str in opens:
                id_match = re.search(r'id=["\']([^"\']+)["\']', attr_str, re.IGNORECASE)
                class_match = re.search(r'class=["\']([^"\']+)["\']', attr_str, re.IGNORECASE)
                label = "div"
                if id_match: label += f'#{id_match.group(1)}'
                elif class_match: label += f'.{class_match.group(1).split()[0]}'
                div_stack.append((i, label))
                if trace: print(f"{i:5} | {'  '*len(div_stack)} OPEN {label}")
            
            # Track DIVs (Close)
            closes = re.findall(r'</div', seg, re.IGNORECASE)
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
