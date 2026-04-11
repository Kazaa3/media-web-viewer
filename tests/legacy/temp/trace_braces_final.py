from pathlib import Path

def find_brace_imbalance():
    app_html = Path("web/app.html")
    content = app_html.read_text(encoding='utf-8')
    
    stack = []
    i = 0
    n = len(content)
    line = 1
    col = 1
    
    while i < n:
        char = content[i]
        
        # Skip single-line comment
        if content[i:i+2] == '//':
            i = content.find('\n', i)
            if i == -1: break
            line += 1
            col = 1
            continue
            
        # Skip multi-line comment
        elif content[i:i+2] == '/*':
            start_i = i
            i = content.find('*/', i)
            if i == -1:
                print(f"Unclosed /* comment starting at line {line}")
                break
            line += content[start_i:i+2].count('\n')
            i += 2
            continue
            
        # Skip strings
        elif char in "'\"`":
            quote = char
            i += 1
            while i < n:
                if content[i] == '\n':
                    line += 1
                    col = 1
                else: col += 1
                    
                if content[i] == '\\':
                    i += 2
                elif content[i] == quote:
                    i += 1
                    break
                else:
                    i += 1
            continue
            
        elif char == '{':
            stack.append(('{', line, col, i))
            i += 1
            col += 1
        elif char == '}':
            if not stack:
                context = content[max(0, i-50):min(n, i+50)].replace('\n', '\\n')
                print(f"Extra '}}' found at index {i}, line {line}, col {col}. Context: ...{context}...")
            else:
                stack.pop()
            i += 1
            col += 1
        elif char == '\n':
            line += 1
            col = 1
            i += 1
        else:
            i += 1
            col += 1
            
    if stack:
        print(f"Unclosed braces left on stack: {len(stack)}")
        for char, l, c, idx in stack[:10]:
            print(f"  '{char}' opened at index {idx}, line {l}, col {c}")

if __name__ == "__main__":
    find_brace_imbalance()
