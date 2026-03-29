import eel
import os
import sys

os.makedirs('/tmp/web', exist_ok=True)
with open('/tmp/web/index.html', 'w') as f:
    f.write('<h1>Test</h1>')

eel.init('/tmp/web')
port = 8400
print(f"Starting Eel on {port} (BLOCKING)...")
try:
    # This should block the script!
    eel.start('index.html', mode=False, block=True, port=port)
    print("eel.start() returned unexpectedly!")
except Exception as e:
    print(f"CRASH: {e}")
except KeyboardInterrupt:
    print("Interrupted.")
