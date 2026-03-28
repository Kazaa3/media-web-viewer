import sys
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))
sys.path.append(str(PROJECT_ROOT / "src"))

import argparse

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
    from tests.engines.suite_config import ConfigSuiteEngine
    from tests.engines.suite_routing import RoutingSuiteEngine
    from tests.engines.suite_scripts import ScriptSuiteEngine
    from tests.engines.suite_i18n import I18nSuiteEngine
    from tests.engines.suite_optimization import OptimizationSuiteEngine
    from tests.engines.suite_complexity import ComplexitySuiteEngine
    from tests.engines.suite_styles import StylesSuiteEngine
    from tests.engines.suite_subtitles import SubtitleSuiteEngine
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
    from engines.suite_config import ConfigSuiteEngine
    from engines.suite_routing import RoutingSuiteEngine
    from engines.suite_scripts import ScriptSuiteEngine
    from engines.i18n import I18nSuiteEngine
    from engines.suite_optimization import OptimizationSuiteEngine
    from engines.suite_complexity import ComplexitySuiteEngine
    from engines.suite_styles import StylesSuiteEngine
    from engines.suite_subtitles import SubtitleSuiteEngine

def run_master_diagnostic():
    parser = argparse.ArgumentParser(description="Master Diagnostic Runner")
    parser.add_argument("--basis", action="store_true", help="Run only basis levels (L1-L2)")
    args = parser.parse_args()

    print("="*60)
    print("ULTIMATE MEDIA WEB VIEWER - MASTER DIAGNOSTIC RUNNER")
    if args.basis:
        print("MODE: BASIS ONLY (L1-L2)")
    print("="*60)
    
    suites = [
        UltimateSuiteEngine(), ItemsSuiteEngine(), UISuiteEngine(), EnvSuiteEngine(),
        DatabaseSuiteEngine(), PlayerSuiteEngine(), MediaIntegritySuiteEngine(),
        NetworkIntegrationSuiteEngine(), CodeQualitySuiteEngine(), AutomationSuiteEngine(),
        CastingSuiteEngine(), AudioplayerSuiteEngine(), PlaylistSuiteEngine(),
        LogbuchSuiteEngine(), ReportingSuiteEngine(), UIIntegritySuiteEngine(),
        ParserSuiteEngine(), EditSuiteEngine(), SidebarSuiteEngine(),
        ConfigSuiteEngine(), RoutingSuiteEngine(),
        ScriptSuiteEngine(), I18nSuiteEngine(), OptimizationSuiteEngine(),
        ComplexitySuiteEngine(), StylesSuiteEngine(), SubtitleSuiteEngine()
    ]
    
    for suite in suites:
        suite.run(basis_only=args.basis)
    
    print("\n" + "="*60)
    print("MASTER DIAGNOSTIC COMPLETE")
    print("="*60)

if __name__ == "__main__":
    run_master_diagnostic()
