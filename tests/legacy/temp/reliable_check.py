import re
from pathlib import Path

content = Path('web/app.html').read_text(encoding='utf-8')
matches = re.finditer(r'<script.*?>\n?(.*?)\n?<\/script>', content, re.DOTALL)

def check_script(code, start_line):
    stack = []
    in_template = False
    in_string = False
    string_char = ''
    escaped = False
    
    lines = code.splitlines()
    for i, line in enumerate(lines):
        line_no = start_line + i
        for j, char in enumerate(line):
            if escaped: escaped = False; continue
            if char == '\\': escaped = True; continue
            if char == '`':
                if not in_string: in_template = not in_template
                continue
            if char in ["'", '"']:
                if not in_template:
                    if not in_string: in_string = True; string_char = char
                    elif string_char == char: in_string = False
                continue
            
            if not in_string and not in_template:
                if char in ['(', '{', '[']:
                    stack.append((char, line_no, j+1))
                elif char in [')', '}', ']']:
                    if not stack:
                        print(f"Extra closing {char} at L{line_no}:{j+1}")
                    else:
                        top, l, c = stack.pop()
                        if (top == '(' and char != ')') or \
                           (top == '{' and char != '}') or \
                           (top == '[' and char != ']'):
                            # Put back and report mismatch?
                            pass
    return stack

# Find line numbers of script tags
script_starts = [m.start() for m in re.finditer(r'<script.*?>', content)]
line_numbers = [content[:s].count('\n') + 1 for s in script_starts]

for i, m in enumerate(re.finditer(r'<script.*?>\n?(.*?)\n?<\/script>', content, re.DOTALL)):
    code = m.group(1)
    start_l = line_numbers[i]
    # print(f"Checking Script starting at L{start_l}...")
    errors = check_script(code, start_l)
    if errors:
        print(f"UNCLOSED in script at L{start_l}:")
        for char, l, c in errors:
            print(f"  {char} at L{l}:{c}")
