import re

def find_extra_paren(text):
    stack = []
    lines = text.split('\n')
    
    # We must skip strings and regex literals properly!
    # Because ( and ) are frequent in strings.
    
    in_s_quote = False
    in_d_quote = False
    in_backtick = False
    
    for i, line in enumerate(lines):
        clean_line = ""
        # Super-simplified string removal for finding ( and )
        # (Assuming no multi-line strings for simplicity except backticks)
        for j, char in enumerate(line):
             if char == "'" and not in_d_quote and not in_backtick: in_s_quote = not in_s_quote
             elif char == '"' and not in_s_quote and not in_backtick: in_d_quote = not in_d_quote
             elif char == '`': in_backtick = not in_backtick # Simple backtick toggle
             
             if not (in_s_quote or in_d_quote or in_backtick):
                 if char == '(':
                     stack.append((i+1, j+1))
                 elif char == ')':
                     if not stack:
                         print(f'Line {i+6399}: UNMATCHED CLOSING PARENTHESIS: {line.strip()}')
                     else:
                         stack.pop()

with open('/tmp/main_script.js', 'r') as f:
    find_extra_paren(f.read())
