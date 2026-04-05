from pathlib import Path

content = Path('web/app.html').read_text(encoding='utf-8')
lines = content.splitlines()
p = 0
for i, line in enumerate(lines):
    old_p = p
    num_open = line.count('(')
    num_close = line.count(')')
    p += num_open - num_close
    if p != old_p and p == 1 and old_p == 0:
        print(f"FIRST Imbalance at L{i+1}: {line.strip()}")
        # We don't break, keep scanning to find where it stays 1
