import re
from bs4 import BeautifulSoup

filepath = '/home/xc/#Coding/gui_media_web_viewer/web/app.html'

with open(filepath, 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

def is_raw_text(node):
    if node.parent.name in ['script', 'style', 'code', 'pre']:
        return False
    if 'data-i18n' in node.parent.attrs:
        return False
    # Check if any ancestor has data-i18n (though usually we want it on the closest element)
    curr = node.parent
    while curr:
        if 'data-i18n' in curr.attrs:
            return False
        curr = curr.parent
    
    text = str(node).strip()
    if not text:
        return False
    if len(text) < 2: # Skip single chars like ':' or '-'
        return False
    if text.startswith('var ') or text.startswith('function '): # Heuristic for script fragments if soup fails
        return False
    
    return True

raw_nodes = []
for text_node in soup.find_all(string=True):
    if is_raw_text(text_node):
        raw_nodes.append({
            'tag': text_node.parent.name,
            'text': str(text_node).strip(),
            'line': text_node.parent.sourceline if hasattr(text_node.parent, 'sourceline') else '?'
        })

print(f"Found {len(raw_nodes)} potential raw text nodes.")
for i, node in enumerate(raw_nodes[:50]): # Show first 50
    print(f"{i+1}. [{node['tag']}] Line {node['line']}: {node['text']}")
