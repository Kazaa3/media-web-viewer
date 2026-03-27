import sys

def audit_divs(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    balance = 0
    stack = []
    
    tab_ids = [
        'player-tab', 'library-tab', 'item-tab', 'search-tab', 
        'transcode-tab', 'status-tab', 'parser-tab', 'tests-tab', 'reporting-tab'
    ]
    
    for i, line in enumerate(lines):
        line_num = i + 1
        opens = line.count('<div')
        closes = line.count('</div')
        
        balance += opens - closes
        
        if opens > 0:
            for _ in range(opens):
                stack.append(line_num)
        
        if closes > 0:
            for _ in range(closes):
                if stack:
                    stack.pop()
        
        # Check specific containers
        if 'class="layout-container"' in line:
            print(f"L{line_num}: layout-container START, balance: {balance}")
        
        for tid in tab_ids:
            if f'id="{tid}"' in line:
                print(f"L{line_num}: {tid} START, balance: {balance}")
        
        if line_num == 5375:
            print(f"L{line_num}: Footer start, balance: {balance}")
            
    print(f"Final balance: {balance}")
    if balance != 0:
        print(f"Imbalance detected! Stack size: {len(stack)}")
        if stack:
             print("Last 10 opened divs (L#):", stack[-10:])

if __name__ == "__main__":
    audit_divs(sys.argv[1])
