from pathlib import Path

content = Path('web/app.html').read_text(encoding='utf-8')
lines = content.splitlines()[5879-1:10780]
b = 0
for i, line in enumerate(lines):
    # Ignore escaped brackets in regex
    # Actually, simpler to just count real brackets in a clean line
    clean = ''
    esc = False
    in_regex = False
    for char in line:
        if esc:
            esc = False
            continue
        if char == '\\':
            esc = True
            continue
        if char == '/':
            # Simplification: if we see / it might be a regex start?
            # but it could be division.
            pass
        clean += char
    
    b += clean.count('[') - clean.count(']')
    
    if b < 0:
        print(f"L{i+5879} [Bracket Bal={b}]: {line.strip()}")
        b = 0

if b != 0:
    print(f"Final global imbalance BRACKETS: {b}")
