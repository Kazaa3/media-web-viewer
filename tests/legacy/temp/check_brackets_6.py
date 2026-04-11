from pathlib import Path

content = Path('web/app.html').read_text(encoding='utf-8')
lines = content.splitlines()[5879-1:10780]
b = 0
for i, line in enumerate(lines):
    num_open = line.count('[')
    num_close = line.count(']')
    b += num_open - num_close
    if b < 0:
        print(f"L{i+5879} [Bracket Bal={b}]: {line.strip()}")
        b = 0

if b != 0:
    print(f"Final imbalance BRACKETS: {b}")
