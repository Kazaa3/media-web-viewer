import re
from pathlib import Path

content = Path('web/app.html').read_text(encoding='utf-8')
matches = list(re.finditer(r'<script.*?>\s*(.*?)\s*<\/script>', content, re.DOTALL))
script = matches[6].group(1) # L1519 script

stack = []
for i, line in enumerate(script.splitlines()):
    for char in line:
        if char == '{': stack.append(i)
        elif char == '}':
            if stack: stack.pop()
if stack:
    print("UNCLOSED BRACES in Script #3:")
    for l in stack: print(f"  Line starting at {l}")
else:
    print("Script #3 braces matched!")
