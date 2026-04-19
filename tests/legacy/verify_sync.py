import sys
import os
import json
import time
from pathlib import Path

# Setup path to include src/
from src.core.config_master import PROJECT_ROOT, DB_FILENAME, TEST_DIR, DATA_DIR
if str(PROJECT_ROOT) not in sys.path:

# Mock Eel to avoid starting a real server during unit tests
class MockEel:
    def expose(self, func):
        return func

import eel
eel.expose = MockEel().expose

import src.core.main as main

def test_json_sanitization():
    print("\n--- Testing JSON Sanitization ---")
    data = {
        "valid": "Standard String",
        "nested": {"key": "Value with \xd8\xaa (invalid surrogate or similar)"},
        "list": ["item1", "item2 \ud83d\ude00"]
    }
    
    # Simulate a "dirty" string that might cause UTF-8 issues
    # Python 3 strings are always unicode, but let's test the 'replace' logic
    dirty_str = "Invalid: \ud800" # Lone surrogate
    sanitized_str = main.sanitize_json_utf8(dirty_str)
    print(f"Original: {repr(dirty_str)} -> Sanitized: {repr(sanitized_str)}")
    
    sanitized_data = main.sanitize_json_utf8(data)
    # Verify it can be dumped to JSON without errors
    json_str = json.dumps(sanitized_data)
    print("Successfully serialized to JSON.")
    return True

def test_rtt_ping_and_confirmation():
    print("\n--- Testing RTT Ping and Confirmation Logic ---")
    
    test_cases = [
        {"type": "dict", "data": {"key": "value"}},
        {"type": "dict_of_dict", "data": {"parent": {"child": 123}}},
        {"type": "list_of_dicts", "data": [{"id": 1}, {"id": 2}]}
    ]
    
    for case in test_cases:
        print(f"Testing {case['type']}...")
        result = main.rtt_ping(case['data'])
        if result['status'] == 'pong' and result['echo'] == case['data']:
            print(f"  [OK] Ping echo matches for {case['type']}")
        else:
            print(f"  [FAIL] Ping failed for {case['type']}: {result}")
            return False
            
    # Test confirmation
    print("Testing Confirm Receipt...")
    sync_result = main.confirm_receipt("UNIT_TEST_SYNC")
    if sync_result['status'] == 'log_noted':
        print("  [OK] Confirmation logged.")
    else:
        print("  [FAIL] Confirmation failed.")
        return False
        
    return True

if __name__ == "__main__":
    print("Starting Synchronization & RTT Verification Tests...")
    success = True
    success &= test_json_sanitization()
    success &= test_rtt_ping_and_confirmation()
    
    if success:
        print("\nALL TESTS PASSED SUCCESSFULLY.")
        sys.exit(0)
    else:
        print("\nSOME TESTS FAILED.")
        sys.exit(1)
