from pathlib import Path

content = Path('web/app.html').read_text(encoding='utf-8')
lines = content.splitlines()[5589-1:5629]

stack = [] # Store (char, line, col)
in_template = False
in_string = False
string_char = ''
escaped = False

for i, line in enumerate(lines):
    line_no = i + 5589
    for j, char in enumerate(line):
        if escaped: escaped = False; continue
        if char == '\\': escaped = True; continue
        if char == '`':
            if not in_string: in_template = not in_template
            continue
        if char in ["'", '"']:
            if not in_template:
                if not in_string: in_string = True; string_char = char
                elif string_char == char: in_string = False
            continue
        
        if not in_string and not in_template:
            if char in ['(', '{', '[']:
                stack.append((char, line_no, j+1))
            elif char in [')', '}', ']']:
                if not stack: print(f"Extra closing {char} at L{line_no}:{j+1}")
                else: stack.pop()

if stack:
    print("UNCLOSED STRUCTURES in Script #5:")
    for char, l, c in stack:
        print(f"  {char} at L{l}:{c}")
else:
    print("Script #5 matched!")
