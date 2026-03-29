from pathlib import Path

content = Path('web/app.html').read_text(encoding='utf-8')
lines = content.splitlines()[5879-1:10780]

b = 0
stack = [] # (line_no, text)
for i, line in enumerate(lines):
    line_no = i + 5879
    # ignore strings
    clean = ''
    in_s = False
    esc = False
    for char in line:
        if esc: esc = False; continue
        if char == '\\': esc = True; continue
        if char == '"' or char == "'": in_s = not in_s; continue
        if not in_s: clean += char
    
    num_open = clean.count('{')
    num_close = clean.count('}')
    
    for _ in range(num_open):
        stack.append(line_no)
        b += 1
    for _ in range(num_close):
        if stack: stack.pop()
        b -= 1
        if b < 0:
            print(f"L{line_no}: Negative balance!")
            b = 0

if b != 0:
    print(f"Final imbalance: {b}")
    print("Unclosed braces started at lines:")
    for l in stack:
        print(f"  L{l}")
