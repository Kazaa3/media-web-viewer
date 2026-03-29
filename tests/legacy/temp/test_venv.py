import sys
import os
print(f"PID: {os.getpid()}")
print(f"Python: {sys.executable}")
print("Importing eel...")
import eel
print("Importing bottle...")
import bottle
print("Importing psutil...")
import psutil
print("All imports SUCCESS")
