import eel
import os
import time
import socket

# Minimal web dir
os.makedirs('/tmp/web', exist_ok=True)
with open('/tmp/web/index.html', 'w') as f:
    f.write('<h1>Test</h1>')

eel.init('/tmp/web')

port = 8399
print(f"Starting Eel on {port}...")
try:
    eel.start('index.html', mode=False, block=False, port=port)
    print("eel.start() returned.")
    
    # Check port
    time.sleep(1)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        res = s.connect_ex(('127.0.0.1', port))
        print(f"Socket connection result: {res} (0 means success)")
except Exception as e:
    print(f"CRASH: {e}")
