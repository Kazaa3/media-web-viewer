import sys
import subprocess

print("Starting app...")
p = subprocess.Popen([sys.executable, "main.py"])
p.wait()
