import re

def find_extra_paren_precise(text, start_line):
    stack = []
    lines = text.split('\n')
    
    for i, line in enumerate(lines):
        # Handle strings
        l = line
        l = re.sub(r'\'(.*?)\'', '', l)
        l = re.sub(r'"(.*?)"', '', l)
        l = re.sub(r'`(.*?)`', '', l)
        
        for char in l:
            if char == '(': stack.append(i+start_line)
            elif char == ')':
                if not stack:
                    print(f'Line {i+start_line}: UNMATCHED CLOSING PAREN: {line.strip()}')
                else:
                    stack.pop()

with open('/tmp/main_script.js', 'r') as f:
    find_extra_paren_precise(f.read(), 6399)
