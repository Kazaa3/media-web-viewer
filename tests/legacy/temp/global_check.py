from pathlib import Path

content = Path('web/app.html').read_text(encoding='utf-8')
lines = content.splitlines()
p = 0
for i, line in enumerate(lines):
    old_p = p
    # ignore parens in HTML comments? No, browser usually doesn't care.
    p += line.count('(') - line.count(')')
    if p != old_p:
        # Check for break point
        pass
if p != 0:
    print(f"Global imbalance: {p}")
