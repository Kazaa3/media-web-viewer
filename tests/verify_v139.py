import sys
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT / "src"))

os.environ["MWV_TEST_MODE"] = "1"
os.environ["UNIT_TESTING"] = "1"

from core.config_master import GLOBAL_CONFIG

def verify_v139():
    print("="*60)
    print("VERIFYING v1.39 UI CONFIGURATION CHANGES")
    print("="*60)
    
    ui_settings = GLOBAL_CONFIG.get('ui_settings', {})
    matrix = ui_settings.get('ui_visibility_matrix', {})
    
    # Check 1: kill_on_startup
    kos = ui_settings.get('kill_on_startup')
    print(f"Check 1: kill_on_startup == False? -> {kos == False} (found: {kos})")
    assert kos == False, "kill_on_startup must be False for accelerated boot."
    
    # Check 2: media sub-menu (contextual_pill_nav)
    media_nav = matrix.get('media', {}).get('contextual_pill_nav')
    print(f"Check 2: media.contextual_pill_nav == True? -> {media_nav == True} (found: {media_nav})")
    assert media_nav == True, "media contextual_pill_nav must be True for visible sub-menus."
    
    # Check 3: library sidebar (sidebar_visible)
    lib_sidebar = matrix.get('library', {}).get('sidebar_visible')
    print(f"Check 3: library.sidebar_visible == False? -> {lib_sidebar == False} (found: {lib_sidebar})")
    assert lib_sidebar == False, "library sidebar_visible must be False by default."

    # Check 4: media sidebar (sidebar_visible)
    media_sidebar = matrix.get('media', {}).get('sidebar_visible')
    print(f"Check 4: media.sidebar_visible == False? -> {media_sidebar == False} (found: {media_sidebar})")
    assert media_sidebar == False, "media sidebar_visible must be False by default."

    print("\n" + "="*60)
    print("v1.39 CONFIGURATION VERIFICATION PASSED")
    print("="*60)

if __name__ == "__main__":
    try:
        verify_v139()
    except AssertionError as e:
        print(f"\n[FAIL] {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        sys.exit(1)
