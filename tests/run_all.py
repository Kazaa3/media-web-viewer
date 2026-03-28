import sys
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))
sys.path.append(str(PROJECT_ROOT / "src"))

# Import all suites
try:
    from tests.engines.suite_ultimate import UltimateSuiteEngine
    from tests.engines.suite_items import ItemsSuiteEngine
    from tests.engines.suite_ui import UISuiteEngine
    from tests.engines.suite_env import EnvSuiteEngine
    from tests.engines.suite_database import DatabaseSuiteEngine
    from tests.engines.suite_player import PlayerSuiteEngine
    from tests.engines.suite_media_integrity import MediaIntegritySuiteEngine
    from tests.engines.suite_network import NetworkIntegrationSuiteEngine
    from tests.engines.suite_quality import CodeQualitySuiteEngine
    from tests.engines.suite_automation import AutomationSuiteEngine
    from tests.engines.suite_casting import CastingSuiteEngine
    from tests.engines.suite_audioplayer import AudioplayerSuiteEngine
    from tests.engines.suite_playlist import PlaylistSuiteEngine
    from tests.engines.suite_logbuch import LogbuchSuiteEngine
    from tests.engines.suite_reporting import ReportingSuiteEngine
    from tests.engines.suite_ui_integrity import UIIntegritySuiteEngine
    from tests.engines.suite_parser import ParserSuiteEngine
    from tests.engines.suite_edit import EditSuiteEngine
    from tests.engines.suite_sidebar import SidebarSuiteEngine
    from tests.engines.suite_options import OptionsSuiteEngine
except ImportError:
    # Fallback for direct execution in engines dir or similar
    from engines.suite_ultimate import UltimateSuiteEngine
    from engines.suite_items import ItemsSuiteEngine
    from engines.suite_ui import UISuiteEngine
    from engines.suite_env import EnvSuiteEngine
    from engines.suite_database import DatabaseSuiteEngine
    from engines.suite_player import PlayerSuiteEngine
    from engines.suite_media_integrity import MediaIntegritySuiteEngine
    from engines.suite_network import NetworkIntegrationSuiteEngine
    from engines.suite_quality import CodeQualitySuiteEngine
    from engines.suite_automation import AutomationSuiteEngine
    from engines.suite_casting import CastingSuiteEngine
    from engines.suite_audioplayer import AudioplayerSuiteEngine
    from engines.suite_playlist import PlaylistSuiteEngine
    from engines.suite_logbuch import LogbuchSuiteEngine
    from engines.suite_reporting import ReportingSuiteEngine
    from engines.suite_ui_integrity import UIIntegritySuiteEngine
    from engines.suite_parser import ParserSuiteEngine
    from engines.suite_edit import EditSuiteEngine
    from engines.suite_sidebar import SidebarSuiteEngine
    from engines.suite_options import OptionsSuiteEngine

def run_master_diagnostic():
    print("="*60)
    print("ULTIMATE MEDIA WEB VIEWER - MASTER DIAGNOSTIC RUNNER")
    print("="*60)
    
    UltimateSuiteEngine().run_all()
    ItemsSuiteEngine().run_all()
    UISuiteEngine().run_all()
    EnvSuiteEngine().run_all()
    DatabaseSuiteEngine().run_all()
    PlayerSuiteEngine().run_all()
    MediaIntegritySuiteEngine().run_all()
    NetworkIntegrationSuiteEngine().run_all()
    CodeQualitySuiteEngine().run_all()
    AutomationSuiteEngine().run_all()
    CastingSuiteEngine().run_all()
    AudioplayerSuiteEngine().run_all()
    PlaylistSuiteEngine().run_all()
    LogbuchSuiteEngine().run_all()
    ReportingSuiteEngine().run_all()
    UIIntegritySuiteEngine().run_all()
    ParserSuiteEngine().run_all()
    EditSuiteEngine().run_all()
    SidebarSuiteEngine().run_all()
    OptionsSuiteEngine().run_all()
    
    print("\n" + "="*60)
    print("MASTER DIAGNOSTIC COMPLETE")
    print("="*60)

if __name__ == "__main__":
    run_master_diagnostic()
