import sys

def audit_divs(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    balance = 0
    
    for i, line in enumerate(lines):
        line_num = i + 1
        opens = line.count('<div')
        closes = line.count('</div')
        
        old_balance = balance
        balance += opens - closes
        
        if balance < 0:
            print(f"L{line_num}: Balance became NEGATIVE ({balance}). Content: {line.strip()}")
            balance = 0 # reset for further search? No, keep it negative to see total count
            
    print(f"Final balance: {balance}")

if __name__ == "__main__":
    audit_divs(sys.argv[1])
