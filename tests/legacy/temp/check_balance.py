with open('/tmp/main_script.js', 'r') as f:
    text = f.read()
    
    opens = text.count('{')
    closes = text.count('}')
    print(f'Braces: {opens} vs {closes} (Delta: {opens - closes})')
    
    popens = text.count('(')
    pcloses = text.count(')')
    print(f'Parentheses: {popens} vs {pcloses} (Delta: {popens - pcloses})')
    
    bopens = text.count('[')
    bcloses = text.count(']')
    print(f'Brackets: {bopens} vs {bcloses} (Delta: {bopens - bcloses})')
