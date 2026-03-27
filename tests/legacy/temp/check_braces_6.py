from pathlib import Path

content = Path('web/app.html').read_text(encoding='utf-8')
lines = content.splitlines()[5879-1:10780]
b = 0
for i, line in enumerate(lines):
    b += line.count('{') - line.count('}')
    if b < 0:
        print(f"L{i+5879} [Balance={b} NEGATIVE!]: {line.strip()}")
        b = 0

if b != 0:
    print(f"Final imbalance BRACES: {b}")
