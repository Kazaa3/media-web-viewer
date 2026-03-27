from pathlib import Path

content = Path('web/app.html').read_text(encoding='utf-8')
lines = content.splitlines()
p = 0
for i, line in enumerate(lines):
    old_p = p
    num_open = line.count('(')
    num_close = line.count(')')
    p += num_open - num_close
    if p < 0:
        print(f"L{i+1} [Balance={p} NEGATIVE!]: {line.strip()}")
        p = 0
    if i == len(lines)-1 and p != 0:
        print(f"Final global imbalance: {p}")

# I will also look at the very end of the file
print(f"Line 10780: {lines[10780-1]}")
print(f"Line 10781: {lines[10781-1]}")
print(f"Line 10782: {lines[10782-1]}")
