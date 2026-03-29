import re
from pathlib import Path

content = Path('web/app.html').read_text(encoding='utf-8')
match = list(re.finditer(r'<script.*?>\n(.*?)\n?<\/script>', content, re.DOTALL))
script = match[3].group(1)
start_l = 1519

b = 0
stack = []
in_string = False
in_template = False
string_char = ''
escaped = False

lines = script.splitlines()
for i, line in enumerate(lines):
    line_no = i + start_l
    raw_chars = list(line)
    j = 0
    while j < len(raw_chars):
        char = raw_chars[j]
        if escaped: escaped = False; j += 1; continue
        if char == '\\': escaped = True; j += 1; continue
        if char == '`':
            if not in_string: in_template = not in_template
            j += 1; continue
        if char in ["'", '"']:
            if not in_template:
                if not in_string: in_string = True; string_char = char
                elif string_char == char: in_string = False
            j += 1; continue
        
        if not in_string and not in_template:
            if char == '{':
                stack.append(line_no)
                b += 1
            elif char == '}':
                if not stack: print(f"Extra closing }} at L{line_no}:{j+1}")
                else:
                    stack.pop()
                    b -= 1
        j += 1

if b != 0:
    for l in stack: print(f"  Unclosed from L{l}")
else:
    print("Script #3 is clean!")
