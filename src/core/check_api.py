import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from src.core.api_testing import get_environment_inventory
inventory = get_environment_inventory()
print(f"Status: {inventory.get('status')}")
print(f"Count: {inventory.get('count')}")
if inventory.get('packages'):
    print(f"First 5 packages: {inventory['packages'][:5]}")
