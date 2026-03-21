import re

def find_extra_bracket(text):
    # Remove strings and comments
    text = re.sub(r'//.*', '', text)
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    text = re.sub(r'\'(.*?)\'', '', text, flags=re.DOTALL)
    text = re.sub(r'"(.*?)"', '', text, flags=re.DOTALL)
    text = re.sub(r'`(.*?)`', '', text, flags=re.DOTALL)
    
    # Trace brackets
    lines = text.split('\n')
    count = 0
    for i, line in enumerate(lines):
        for char in line:
            if char == '[': count += 1
            if char == ']': count -= 1
            if count < 0:
                print(f'Line {i+6399}: Extra closing bracket found!')
                count = 0

with open('/tmp/main_script.js', 'r') as f:
    find_extra_bracket(f.read())
