from pathlib import Path

content = Path('web/app.html').read_text(encoding='utf-8')
lines = content.splitlines()[5879-1:10780]
p = 0
for i, line in enumerate(lines):
    old_p = p
    num_open = line.count('(')
    num_close = line.count(')')
    p += num_open - num_close
    if p < 0:
        print(f"L{i+5879} [Balance={p}]: {line.strip()}")
        p = 0 # reset to continue

if p != 0:
    print(f"Final imbalance: {p}")
