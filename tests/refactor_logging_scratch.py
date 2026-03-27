import sys
import re

def refactor_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    # Find the line where 'log = get_logger("main")' is defined to avoid replacing before it
    log_defined_line = -1
    for i, line in enumerate(lines):
        if 'log = get_logger("main")' in line:
            log_defined_line = i
            break
    
    for i, line in enumerate(lines):
        if i <= log_defined_line:
            new_lines.append(line)
            continue
        
        # Replace logging calls
        new_line = re.sub(r'\blogging\.(info|error|warning|debug|critical)\(', r'log.\1(', line)
        
        # Replace specific print calls found in main.py
        if 'print(f"read_file error:' in new_line:
            new_line = new_line.replace('print(', 'log.error(')
        
        new_lines.append(new_line)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    refactor_file(sys.argv[1])
