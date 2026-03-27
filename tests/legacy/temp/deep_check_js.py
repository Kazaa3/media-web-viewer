from pathlib import Path

content = Path('web/app.html').read_text(encoding='utf-8')
lines = content.splitlines()[5879-1:10780]

stack = [] # Store (char, line, col)
in_template = False
in_string = False
string_char = ''
escaped = False

for i, line in enumerate(lines):
    line_no = i + 5879
    for j, char in enumerate(line):
        if escaped:
            escaped = False
            continue
        if char == '\\':
            escaped = True
            continue
        if char == '`':
            if not in_string: in_template = not in_template
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
            if char in ['(', '{', '[']:
                stack.append((char, line_no, j+1))
            elif char in [')', '}', ']']:
                if not stack:
                    print(f"Extra closing {char} at L{line_no}:{j+1}")
                else:
                    top, l, c = stack.pop()
                    if (top == '(' and char != ')') or \
                       (top == '{' and char != '}') or \
                       (top == '[' and char != ']'):
                        print(f"Mismatch: {top} at L{l}:{c} closed by {char} at L{line_no}:{j+1}")

if stack:
    print("UNCLOSED STRUCTURES:")
    for char, l, c in stack:
        print(f"  {char} at L{l}:{c}")
else:
    print("Everything matched!")
