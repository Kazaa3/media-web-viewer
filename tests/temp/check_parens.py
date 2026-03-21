from pathlib import Path

content = Path('web/app.html').read_text(encoding='utf-8')
lines = content.splitlines()
p = 0
for i, line in enumerate(lines):
    if i < 1519 or i >= 2974: continue
    old_p = p
    p += line.count('(')
        # ignore matches in comments or strings (simplification)
    p -= line.count(')')
    if p != old_p:
        # print only if it changed
        pass
    if p < 0:
        print(f"L{i+1}: Negative Pareto balance: {p} | {line}")
        p = 0 # reset to continue

if p != 0:
    print(f"Final imbalance after script 1519-2974: {p}")
