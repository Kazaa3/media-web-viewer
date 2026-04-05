from pathlib import Path

content = Path('web/app.html').read_text(encoding='utf-8')
lines = content.splitlines()[5879-1:10780]
count = 0
for i, line in enumerate(lines):
    # ignore escaped backticks
    clean = line.replace('\\`', '')
    num = clean.count('`')
    count += num
    if count % 2 != 0:
        # print("Odd backticks at L", i+5879)
        pass

print(f"Total backticks in Script #6: {count}")
if count % 2 != 0:
    print("WARNING: Odd number of backticks!")
