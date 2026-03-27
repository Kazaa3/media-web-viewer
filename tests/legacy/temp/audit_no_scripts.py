import sys

def audit_divs(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Remove scripts to avoid false positives
    import re
    content_no_scripts = re.sub(r'<script.*?>.*?</script>', '', content, flags=re.DOTALL)
    
    balance = content_no_scripts.count('<div') - content_no_scripts.count('</div')
    
    print(f"Balance (excluding scripts): {balance}")

if __name__ == "__main__":
    audit_divs(sys.argv[1])
