import re
from pathlib import Path

content = Path('web/app.html').read_text(encoding='utf-8')
match = list(re.finditer(r'<script.*?>\n(.*?)\n?<\/script>', content, re.DOTALL))
script = match[3].group(1) # My index was 3 for 1519.
start_l = 1519

p = 0
stack = []
for i, line in enumerate(script.splitlines()):
    l_no = i + start_l
    for j, char in enumerate(line):
        if char == '(':
            stack.append(l_no)
            p += 1
        elif char == ')':
            if stack: stack.pop(); p -= 1
            else: print(f"Extra ) at L{l_no}")

if p != 0:
    print(f"Final imbalance (: {p}")
    for l in stack: print(f"  Unclosed ( from L {l}")
