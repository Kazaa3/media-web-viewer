from pathlib import Path

content = Path('web/app.html').read_text(encoding='utf-8')
lines = content.splitlines()
p = 0
for i, line in enumerate(lines):
    old_p = p
    num_open = line.count('(')
    num_close = line.count(')')
    p += num_open - num_close
    if num_open != num_close:
        # Check WHICH ONE changed it
        # print first few occurrences
        if i < 100 or i > 10700:
            print(f"L{i+1} [Bal={p}]: {line.strip()}")
