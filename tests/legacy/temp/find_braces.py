import sys

filename = '/home/xc/#Coding/gui_media_web_viewer/web/app.html'
with open(filename, 'r', encoding='utf-8') as f:
    lines = f.readlines()

in_script = False
stack = []
for i, line in enumerate(lines):
    if '<script' in line:
        in_script = True
    if '</script>' in line:
        in_script = False
        if stack:
            print(f"Script block ended at line {i+1} with unclosed braces: {len(stack)}")
            stack = [] # Reset for next block
            
    if not in_script: continue
    
    # Strip comments
    clean_line = line
    if '//' in clean_line:
        clean_line = clean_line[:clean_line.find('//')]
    
    for j, char in enumerate(clean_line):
        if char == '{':
            stack.append((i+1, j+1))
        elif char == '}':
            if stack:
                stack.pop()
            else:
                print(f"Extra closing brace at line {i+1}, col {j+1}: {line.strip()}")

if stack:
    print(f"Unclosed opening braces at end of file ({len(stack)}):")
else:
    print("Brace check completed.")
