from pathlib import Path

content = Path('web/app.html').read_text(encoding='utf-8')
import re
scripts = re.findall(r'<script.*?>\n(.*?)<\/script>', content, re.DOTALL)

def find_imbalance(code):
    stack = []
    i = 0
    while i < len(code):
        char = code[i]
        
        # Handle strings
        if char in ["'", '"']:
            q = char
            i += 1
            while i < len(code) and (code[i] != q or code[i-1] == '\\'):
                i += 1
        # Handle template literals with recursion for ${ }
        elif char == '`':
            i += 1
            while i < len(code) and (code[i] != '`' or code[i-1] == '\\'):
                if code[i:i+2] == '${' and code[i-1] != '\\':
                    # Recursive call or find matching }
                    # For simplicity, we just find the balance of { } inside
                    i += 2
                    sub_b = 1
                    while i < len(code) and sub_b > 0:
                        if code[i] == '{' and code[i-1] != '\\': sub_b += 1
                        if code[i] == '}' and code[i-1] != '\\': sub_b -= 1
                        i += 1
                    i -= 1 # adjust to stay on }
                i += 1
        # Handle comments
        elif code[i:i+2] == '//':
            while i < len(code) and code[i] != '\n': i += 1
        elif code[i:i+2] == '/*':
            while i < len(code) and code[i:i+2] != '*/': i += 1
            i += 1
        # Code structure
        elif char in ['(', '{', '[']:
            stack.append(char)
        elif char in [')', '}', ']']:
            if not stack: return f"Extra {char}"
            top = stack.pop()
            if (top == '(' and char != ')') or \
               (top == '{' and char != '}') or \
               (top == '[' and char != ']'):
                return f"Mismatch: {top} closed by {char}"
        i += 1
    return stack

for idx, script in enumerate(scripts):
    res = find_imbalance(script)
    if res:
        print(f"Script #{idx} IMBLANCE: {res}")
