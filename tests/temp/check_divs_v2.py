
def count_divs(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Simple count
    open_tags = content.count('<div ') + content.count('<div>')
    close_tags = content.count('</div>')
    
    print(f"Total Opening: {open_tags}")
    print(f"Total Closing: {close_tags}")
    print(f"Balance: {open_tags - close_tags}")

    # Track level
    lines = content.splitlines()
    level = 0
    for i, line in enumerate(lines):
        line_num = i + 1
        level += line.count('<div ') + line.count('<div>')
        level -= line.count('</div>')
        if level < 0:
            print(f"Negative level at line {line_num}: {level}")
            # Show context
            start = max(0, i-2)
            end = min(len(lines), i+3)
            for j in range(start, end):
                print(f"{j+1}: {lines[j]}")
            break

count_divs('/home/xc/#Coding/gui_media_web_viewer/web/app.html')
