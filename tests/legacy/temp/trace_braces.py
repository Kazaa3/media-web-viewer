with open('/tmp/main_script.js', 'r') as f:
    lines = f.readlines()

brace_count = 0
for i, line in enumerate(lines):
    # Ignore comments and strings and chars? Too complex.
    # Simple count:
    brace_count += line.count('{')
    brace_count -= line.count('}')
    
    if brace_count < 0:
        print(f'Line {i+1}: Brace count went negative! ({brace_count})')
        # Reset to 0 to find next error
        brace_count = 0

print(f'Final brace count: {brace_count}')
