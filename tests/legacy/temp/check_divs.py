
import sys

def check_div_balance(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    balance = 0
    for i, line in enumerate(lines):
        opens = line.count('<div')
        closes = line.count('</div')
        balance += opens - closes
        if balance < 0:
            print(f"Negative balance at line {i+1}: {balance}")
            # print(line.strip())
            # return
    print(f"Final balance: {balance}")

if __name__ == "__main__":
    check_div_balance(sys.argv[1])
