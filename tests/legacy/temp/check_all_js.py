import re
from pathlib import Path

content = Path('web/app.html').read_text(encoding='utf-8')
scripts = re.split(r'<script.*?>', content)

# skip the first split as it's not inside a script
for i, script_block in enumerate(scripts[1:]):
    # inside script_block until next split or </script>?
    # Re-using findall is safer for content extraction
    pass

scripts = re.findall(r'<script.*?>\n(.*?)<\/script>', content, re.DOTALL)

def check_parens(code):
    p = 0
    in_template = False
    in_string = False
    string_char = ''
    escaped = False
    for char in code:
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
            if char == '(': p += 1
            if char == ')': p -= 1
    return p

for i, script in enumerate(scripts):
    imb = check_parens(script)
    print(f"Script #{i}: Imbalance={imb}")
