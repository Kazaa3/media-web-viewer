from pathlib import Path

content = Path('web/app.html').read_text(encoding='utf-8')
lines = content.splitlines()[5879-1:10780]

b = 0
for i, line in enumerate(lines):
    # Ignore escaped brackets or regex
    clean = ''
    esc = False
    for char in line:
        if esc: esc = False; continue
        if char == '\\': esc = True; continue
        clean += char
    
    b += clean.count('[') - clean.count(']')
    if b < 0:
        print(f"L{i+5879} [Bal={b}]: {line.strip()}")
        b = 0 # reset
