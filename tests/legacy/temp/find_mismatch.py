from pathlib import Path

content = Path('web/app.html').read_text(encoding='utf-8')
import re
# Match only the massive script #6 (starts 5879)
match = list(re.finditer(r'<script.*?>\n(.*?)<\/script>', content, re.DOTALL))
script = match[6].group(1) # My index was 6 or 9. I'll use index based on starting line.
start_l = 5879

stack = []
i = 0
while i < len(script):
    char = script[i]
    line = start_l + script[:i].count('\n')
    
    if char in ["'", '"']:
        q = char; i += 1
        while i < len(script) and (script[i] != q or script[i-1] == '\\'): i += 1
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
    elif script[i:i+2] == '//':
        while i < len(script) and script[i] != '\n': i += 1
    elif script[i:i+2] == '/*':
        i += 2
        while i < len(script) and script[i:i+2] != '*/': i += 1
        i += 1
    elif char in ['(', '{', '[']:
        stack.append((char, line))
    elif char in [')', '}', ']']:
        if not stack:
            print(f"Extra closing {char} at L{line}")
        else:
            top, l = stack.pop()
            if (top == '(' and char != ')') or \
               (top == '{' and char != '}') or \
               (top == '[' and char != ']'):
                print(f"Mismatch: {top} at L{l} closed by {char} at L{line}")
    i += 1
