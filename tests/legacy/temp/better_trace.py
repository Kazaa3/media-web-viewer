from pathlib import Path

content = Path('web/app.html').read_text(encoding='utf-8')
lines = content.splitlines()[5879-1:10780]

b = 0
stack = []
in_string = False
in_template = False
string_char = ''
escaped = False

for i, line in enumerate(lines):
    line_no = i + 5879
    raw_chars = list(line)
    j = 0
    while j < len(raw_chars):
        char = raw_chars[j]
        if escaped: escaped = False; j += 1; continue
        if char == '\\': escaped = True; j += 1; continue
        if char == '`':
            if not in_string: in_template = not in_template
            j += 1; continue
        if char in ["'", '"']:
            if not in_template:
                if not in_string: in_string = True; string_char = char
                elif string_char == char: in_string = False
            j += 1; continue
        
        if not in_string and not in_template:
            # check for regex / ... / ? hard but necessary
            if char == '/':
                if j+1 < len(raw_chars):
                    if raw_chars[j+1] == '/': # line comment
                        break
                    if raw_chars[j+1] == '*': # block comment
                        # skip until */ ?
                        pass
            
            if char == '{':
                stack.append(line_no)
                b += 1
            elif char == '}':
                if not stack:
                    print(f"L{line_no}:{j+1} - Negative balance! Extra '}}'")
                else:
                    stack.pop()
                    b -= 1
        j += 1

if b != 0:
    print(f"Final imbalance: {b}")
    for l in stack: print(f"  Unclosed from L{l}")
