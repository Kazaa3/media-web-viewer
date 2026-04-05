import re
from pathlib import Path

content = Path('web/app.html').read_text(encoding='utf-8')
matches = list(re.finditer(r'<script.*?>\s*(.*?)\s*<\/script>', content, re.DOTALL))
print(f"Found {len(matches)} scripts.")

# The last script (at Line 5879) should be the last match.
script = matches[-1].group(1)
start_l = 5879

stack = []
i = 0
while i < len(script):
    char = script[i]
    line = start_l + script[:i].count('\n')
    
    if char in ["'", '"']:
        q = char; i += 1
        while i < len(script) and (i < len(script) and (script[i] != q or script[i-1] == '\\')): i += 1
    elif char == '`':
        i += 1
        while i < len(script) and (script[i] != '`' or script[i-1] == '\\'):
            if script[i:i+2] == '${' and script[i-1] != '\\':
                i += 2
                sub_b = 1
                while i < len(script) and sub_b > 0:
                    if script[i] == '{' and script[i-1] != '\\': sub_b += 1
                    if script[i] == '}' and script[i-1] != '\\': sub_b -= 1
                    i += 1
                i -= 1
            i += 1
    elif char in ['(', '{', '[']:
        stack.append((char, line))
    elif char in [')', '}', ']']:
        if not stack:
            # Extra closing
            pass
        else:
            top, l = stack.pop()
    i += 1

if stack:
    print("UNCLOSED in last script:")
    for char, l in stack: print(f"  {char} starting at L{l}")
else:
    print("Last script is balanced!")
