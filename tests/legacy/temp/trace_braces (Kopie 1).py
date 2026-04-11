import sys

filename = '/home/xc/#Coding/gui_media_web_viewer/web/app.html'
with open(filename, 'r', encoding='utf-8') as f:
    lines = f.readlines()

in_script = False
stack = []
start_line = 11840
end_line = 11875

for i, line in enumerate(lines):
    line_no = i + 1
    if line_no < 11000: # Fast forward
        # But we must track the stack!
        pass 
    
    # Actually we need to track from the beginning
    if '<script' in line: in_script = True
    if '</script>' in line:
        in_script = False
        stack = []
        
    if not in_script: continue
    
    clean_line = line
    if '//' in clean_line:
        clean_line = clean_line[:clean_line.find('//')]
        
    for j, char in enumerate(clean_line):
        if char == '{':
            stack.append((line_no, j+1))
        elif char == '}':
            if stack:
                stack.pop()
            else:
                if start_line <= line_no <= end_line:
                    print(f"!!! Extra closing brace at line {line_no}: {line.strip()}")
    
    if start_line <= line_no <= end_line:
        print(f"L{line_no:5} | Stack Size: {len(stack)} | {line.strip()}")

print(f"End of range. Stack contents: {stack}")
