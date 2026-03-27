with open('/tmp/main_script.js', 'r') as f:
    lines = f.readlines()

in_single_quote = False
in_double_quote = False
in_backtick = False

for i, line in enumerate(lines):
    # This is a bit naive but good for finding the line
    # Need to skip escaped quotes
    col = 1
    for char in line:
        if char == "'" and not in_double_quote and not in_backtick:
            # Check for escape
            if col > 1 and line[col-2] == '\\':
                pass # Escaped
            else:
                in_single_quote = not in_single_quote
        elif char == '"' and not in_single_quote and not in_backtick:
            if col > 1 and line[col-2] == '\\':
                pass
            else:
                in_double_quote = not in_double_quote
        elif char == '`' and not in_single_quote and not in_double_quote:
            if col > 1 and line[col-2] == '\\':
                pass
            else:
                in_backtick = not in_backtick
        col += 1
    
    # Check if a quote is left open at the end of the line
    # (Strings in JS can span lines with backticks, but ' and " cannot usually)
    if (in_single_quote or in_double_quote) and char != '\\':
       # Actually ' and " cannot span lines unless escaped with \ at the end
       if line.endswith('\\\n') or line.endswith('\\\r\n'):
           pass
       else:
           # If it's open and not escaped at end, it's a bug!
           print(f'Line {i+6399}: Quote left open at end of line! (S:{in_single_quote}, D:{in_double_quote})')
           # Reset for search
           in_single_quote = False
           in_double_quote = False

if in_backtick:
    print('Final: Backtick left open!')
