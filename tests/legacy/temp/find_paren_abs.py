import re

def find_extra_paren_absolute(text):
    # This script will maintain a stack and print the context of the mismatch in the whole file
    stack = []
    
    in_s_quote = False
    in_d_quote = False
    in_backtick = False
    in_comment_s = False
    in_comment_m = False
    
    lines = text.split('\n')
    
    for i, line in enumerate(lines):
        line_no = i + 1
        
        j = 0
        while j < len(line):
            char = line[j]
            next_char = line[j+1] if j+1 < len(line) else ""
            
            # Handle comments
            if not in_s_quote and not in_d_quote and not in_backtick:
                if not in_comment_m and char == '/' and next_char == '/':
                    break # Single line comment, skip rest of line
                if not in_comment_s and char == '/' and next_char == '*':
                    in_comment_m = True
                    j += 2; continue
                if in_comment_m and char == '*' and next_char == '/':
                    in_comment_m = False
                    j += 2; continue
            
            if not (in_comment_s or in_comment_m):
                # Handle strings
                if char == "'" and not in_d_quote and not in_backtick: in_s_quote = not in_s_quote
                elif char == '"' and not in_s_quote and not in_backtick: in_d_quote = not in_d_quote
                elif char == '`' and not in_s_quote and not in_d_quote: in_backtick = not in_backtick
                
                # If NOT in string or comment, check parens
                if not (in_s_quote or in_d_quote or in_backtick or in_comment_m):
                    if char == '(': stack.append(line_no)
                    elif char == ')':
                         if not stack:
                             print(f'Line {line_no}: UNMATCHED CLOSING PARENTHESIS: {line.strip()}')
                         else: stack.pop()
            j += 1
        
        # New line resets single line comment but NOT strings?
        # Backtick can cross lines. S/D quote cannot usually.
        # If S/D quote is open at end of line without backslash, it's a bug too.
        if (in_s_quote or in_d_quote) and (not line.endswith('\\')):
             # This is a bit rough since we don't know if we are inside a script tag
             pass

    for lno in stack:
        print(f'Line {lno}: UNMATCHED OPENING PARENTHESIS')

with open('/home/xc/#Coding/gui_media_web_viewer/web/app.html', 'r', encoding='utf-8') as f:
    find_extra_paren_absolute(f.read())
