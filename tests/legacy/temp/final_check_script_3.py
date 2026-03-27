import re
from pathlib import Path

content = Path('web/app.html').read_text(encoding='utf-8')
match = list(re.finditer(r'<script.*?>\n(.*?)\n?<\/script>', content, re.DOTALL))
script = match[3].group(1)
start_l = 1519

b = 0
in_template = False
in_string = False
string_char = ''
escaped = False

lines = script.splitlines()
for i, line in enumerate(lines):
    line_no = i + start_l
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
            if char == '{': b += 1
            elif char == '}':
                b -= 1
                if b == 0:
                    # print("Balanced at L", line_no)
                    pass

print(f"Final imbalance for Script at L{start_l}: {b}")
