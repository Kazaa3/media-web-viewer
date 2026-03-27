with open('/tmp/main_script.js', 'r') as f:
    text = f.read()

opens = text.count('(')
closes = text.count(')')
print(f'Parentheses: {opens} vs {closes} (Delta: {opens - closes})')

# Brackets
bopens = text.count('[')
bcloses = text.count(']')
print(f'Brackets: {bopens} vs {bcloses} (Delta: {bopens - bcloses})')

# Quotes
q1 = text.count("'")
q2 = text.count('"')
q3 = text.count("`")
print(f'Quotes: Single: {q1}, Double: {q2}, Backtick: {q3}')
