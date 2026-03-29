from pathlib import Path

content = Path('web/app.html').read_text(encoding='utf-8')
lines = content.splitlines()
p = 0
for i, line in enumerate(lines):
    if i < 1519 or i >= 2974: continue
    
    # Simple paren matcher ignoring strings and comments
    # This is a bit rough but should help
    clean_line = ''
    in_string = False
    string_char = ''
    escaped = False
    
    for char in line:
        if escaped:
            escaped = False
            continue
        if char == '\\':
            escaped = True
            continue
        if char in ["'", '"', '`']:
            if not in_string:
                in_string = True
                string_char = char
            elif string_char == char:
                in_string = False
            continue
        if not in_string:
            if char == '/':
                # check for comment? simplified
                pass
            clean_line += char

    old_p = p
    num_open = clean_line.count('(')
    num_close = clean_line.count(')')
    p += num_open - num_close
    
    if p != old_p:
        print(f"L{i+1} [Balance={p}]: {line.strip()}")

if p != 0:
    print(f"Final imbalance for script: {p}")
