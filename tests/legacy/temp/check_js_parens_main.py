from pathlib import Path

content = Path('web/app.html').read_text(encoding='utf-8')
lines = content.splitlines()
p = 0
for i, line in enumerate(lines):
    if i < 5878: continue # Script #6 starts at 5879
    if i >= 10780: continue # ends at 10780
    
    # Improved paren matcher ignoring strings, template literals and comments
    clean_line = ''
    in_string = False
    in_template = False
    string_char = ''
    escaped = False
    
    for char in line:
        if escaped:
            escaped = False
            continue
        if char == '\\':
            escaped = True
            continue
        if char == '`':
            if not in_string:
                in_template = not in_template
            continue
        if char in ["'", '"']:
            if not in_template:
                if not in_string:
                    in_string = True
                    string_char = char
                elif string_char == char:
                    in_string = False
            continue
        if not in_string and not in_template:
            # ignore parens in comments? (simplified)
            clean_line += char

    old_p = p
    num_open = clean_line.count('(')
    num_close = clean_line.count(')')
    p += num_open - num_close
    
    if p < 0:
        print(f"L{i+1} [Balance={p} NEGATIVE!]: {line.strip()}")
        p = 0 # reset
    # We expect p to be 0 at the end if it was 0 at the start of the block

print(f"Final imbalance for Script #6: {p}")
