from pathlib import Path

content = Path('web/app.html').read_text(encoding='utf-8')
lines = content.splitlines()[5879-1:10780]

stack = []
for i, line in enumerate(lines):
    line_no = i + 5879
    clean = ''
    esc = False
    for char in line:
        if esc: esc = False; continue
        if char == '\\': esc = True; continue
        clean += char
    
    for char in clean:
        if char == '[': stack.append(line_no)
        elif char == ']':
            if not stack:
                print(f"EXTRA CLOSING BRACKET ']' at L{line_no}: {line.strip()}")
            else:
                stack.pop()
if stack:
    print("UNCLOSED BRACKETS at lines:")
    for l in stack: print(f"  L{l}")
