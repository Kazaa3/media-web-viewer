from pathlib import Path

content = Path('web/app.html').read_text(encoding='utf-8')
lines = content.splitlines()
p = 0
for i, line in enumerate(lines):
    if i < 1519 or i >= 2974: continue
    old_p = p
    num_open = line.count('(')
    num_close = line.count(')')
    p += num_open - num_close
    if num_open != num_close:
        print(f"L{i+1} [{p}]: {line.strip()}")
