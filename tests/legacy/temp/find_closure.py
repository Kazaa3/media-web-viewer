from pathlib import Path

content = Path('web/app.html').read_text(encoding='utf-8')
lines = content.splitlines()

s_start = 1519
s_end = 2974

stack = []
for i, line in enumerate(lines):
    if i < s_start or i >= s_end: continue
    
    # Very simple count
    for char in line:
        if char == '{':
            stack.append(i+1)
        elif char == '}':
            if stack:
                opened_at = stack.pop()
                if opened_at == 2605:
                    print(f"L2605 was closed at L{i+1}")
            else:
                pass
if stack:
    print("Unclosed:")
    for l in stack: print(f"  {l}")
