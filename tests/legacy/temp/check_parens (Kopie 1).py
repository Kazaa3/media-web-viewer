import re

def check_file(filepath):
    with open(filepath, 'r') as f:
        for i, line in enumerate(f, 1):
            # Only check script blocks or lines with JS-like keywords
            if '(' in line or ')' in line:
                opening = line.count('(')
                closing = line.count(')')
                if opening != closing:
                    # Ignore lines that are likely just HTML tags or multi-line breaks
                    if 'function' in line or 'eel' in line or 'showToast' in line:
                        print(f"Line {i}: ({opening}) vs ({closing}) -> {line.strip()}")

if __name__ == "__main__":
    check_file('web/app.html')
