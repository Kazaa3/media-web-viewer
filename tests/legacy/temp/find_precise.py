import re

def find_extra_bracket_precise(text):
    # This script will maintain a stack and print the context of the mismatch
    stack = []
    # Using a simple parser that handles strings and comments
    # (Simplified for finding the mismatch)
    
    # Pre-parse: Replace strings and comments with placeholders to maintain length?
    # No, just iterate char by char and track state
    
    in_s_quote = False
    in_d_quote = False
    in_backtick = False
    in_s_comment = False
    in_m_comment = False
    
    for i, char in enumerate(text):
        # Skip escaped chars
        if i > 0 and text[i-1] == '\\': continue
        
        if not in_s_comment and not in_m_comment:
            if char == "'" and not in_d_quote and not in_backtick: in_s_quote = not in_s_quote
            elif char == '"' and not in_s_quote and not in_backtick: in_d_quote = not in_d_quote
            elif char == '`' and not in_s_quote and not in_d_quote: in_backtick = not in_backtick
            
        if not in_s_quote and not in_d_quote and not in_backtick:
            if char == '/' and i+1 < len(text) and text[i+1] == '/': in_s_comment = True
            elif char == '/' and i+1 < len(text) and text[i+1] == '*': in_m_comment = True
            elif char == '\n': in_s_comment = False
            elif char == '*' and i+1 < len(text) and text[i+1] == '/': in_m_comment = False
            
        if not (in_s_quote or in_d_quote or in_backtick or in_s_comment or in_m_comment):
            if char == '[':
                stack.append(i)
            elif char == ']':
                if not stack:
                    # Mismatch!
                    print(f'Mismatch at index {i}:')
                    prefix = text[max(0, i-40):i]
                    suffix = text[i:min(len(text), i+40)]
                    print(f'...{prefix}--> {char} <--{suffix}...')
                else:
                    stack.pop()

with open('/tmp/main_script.js', 'r') as f:
    find_extra_bracket_precise(f.read())
