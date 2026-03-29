import re

def check_brackets_robust(text):
    # Remove single line comments
    text = re.sub(r'//.*', '', text)
    # Remove multi line comments
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    
    # Remove strings
    text = re.sub(r'\'(.*?)\'', '', text, flags=re.DOTALL)
    text = re.sub(r'"(.*?)"', '', text, flags=re.DOTALL)
    text = re.sub(r'`(.*?)`', '', text, flags=re.DOTALL)
    
    o = text.count('[')
    c = text.count(']')
    print(f'Robust Brackets: {o} vs {c} (Delta: {o - c})')

with open('/tmp/main_script.js', 'r') as f:
    check_brackets_robust(f.read())
