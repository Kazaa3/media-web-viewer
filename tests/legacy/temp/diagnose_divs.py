import re
import os

def check_div_balance(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Find tab content start/end lines
    # Using a simple heuristic: id=".*-panel" class="tab-content"
    tab_starts = []
    for i, line in enumerate(lines):
        if 'class="tab-content"' in line and 'id="' in line:
            tab_starts.append(i)
    
    tab_starts.sort()
    
    results = []
    
    for i in range(len(tab_starts)):
        start_line = tab_starts[i]
        # End line is the start of next tab or end of file (heuristic)
        end_line = tab_starts[i+1] if i+1 < len(tab_starts) else len(lines)
        
        # Refine end_line: search for the last </div> before the next tab that closes the tab-content
        # Or just count within the range and see delta
        
        tab_id_match = re.search(r'id="([^"]+)"', lines[start_line])
        tab_id = tab_id_match.group(1) if tab_id_match else f"unknown-{start_line}"
        
        open_divs = 0
        close_divs = 0
        
        for j in range(start_line, end_line):
            line = lines[j]
            open_divs += line.count('<div')
            close_divs += line.count('</div')
            
        results.append({
            "id": tab_id,
            "start": start_line + 1,
            "open": open_divs,
            "close": close_divs,
            "delta": open_divs - close_divs
        })

    print(f"{'Tab ID':<50} | {'Start':<7} | {'Open':<5} | {'Close':<5} | {'Delta':<5}")
    print("-" * 85)
    for res in results:
        print(f"{res['id']:<50} | {res['start']:<7} | {res['open']:<5} | {res['close']:<5} | {res['delta']:<5}")

    # Total file balance
    total_open = sum(line.count('<div') for line in lines)
    total_close = sum(line.count('</div') for line in lines)
    print("-" * 85)
    print(f"{'TOTAL FILE':<50} | {'-':<7} | {total_open:<5} | {total_close:<5} | {total_open - total_close:<5}")

if __name__ == "__main__":
    check_div_balance("/home/xc/#Coding/gui_media_web_viewer/web/app.html")
