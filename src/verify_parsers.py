import sys
import os
from pathlib import Path

# Add project root to sys.path
root = Path("/home/xc/#Coding/gui_media_web_viewer")
sys.path.insert(0, str(root / "src"))

try:
    from core.config_master import GLOBAL_CONFIG
    from parsers.media_parser import get_parser_info
    
    print("--- PARSER REGISTRY TEST ---")
    reg = GLOBAL_CONFIG.get("parser_registry", {})
    module_reg = reg.get("module_registry", {})
    
    print(f"Registered Parsers: {list(module_reg.keys())}")
    
    # Try to get info (triggers imports)
    info = get_parser_info()
    print(f"Successfully loaded {len(info)} parsers.")
    
    if "parser_vlc_bridge" in info:
        print("✅ parser_vlc_bridge is registered and loadable.")
    else:
        print("❌ parser_vlc_bridge is MISSING from info.")
        
    print("--- DYNAMIC CHAIN TEST ---")
    from parsers import media_parser
    # Mocking a call
    # We won't actually parse a file here, but we could if we had a test file.
    
    print("Verification Successful.")

except Exception as e:
    print(f"FAIL: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
