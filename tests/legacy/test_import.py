import sys
import os
from unittest.mock import MagicMock

print("🚀 Starting minimal import test...")

# Mock eel
print("🎭 Mocking eel...")
mock_eel = MagicMock()
sys.modules['eel'] = mock_eel

print("📦 Importing src.core.db...")
try:
    from src.core import db
    print("✅ Imported src.core.db")
except Exception as e:
    print(f"❌ Failed to import src.core.db: {e}")

print("📦 Importing src.core.main...")
try:
    from src.core import main as backend
    print("✅ Imported src.core.main")
except Exception as e:
    print(f"❌ Failed to import src.core.main: {e}")

print("🏁 End of minimal import test.")
