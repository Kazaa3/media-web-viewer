try:
    from tests.engines.test_base import DiagnosticEngine, DiagnosticResult
except ImportError:
    from test_base import DiagnosticEngine, DiagnosticResult

class AdvancedPlayerSuite(DiagnosticEngine):
    """
    @brief Verification of 10+ advanced playback modes and toolchain bridges.
    """
    def __init__(self):
        super().__init__("Advanced Player & Toolchain")

    def level_1_mode_routing_cardinality(self) -> DiagnosticResult:
        """Checks if the mode router supports the expanded cardinality (10+ modes)."""
        from src.core.mode_router import get_mode_description
        modes = ['direct_play', 'mse', 'hls_fmp4', 'vlc_bridge', 'mpv_wasm', 
                 'mpv_native', 'vlc_native', 'dash', 'webtorrent', 'hls_native']
        
        for m in modes:
            desc = get_mode_description(m)
            if "Unbekannter Modus" in desc:
                return DiagnosticResult(1, "Mode Routing", "FAIL", f"Mode '{m}' has no description.")
        return DiagnosticResult(1, "Mode Routing", "PASS", f"Verified {len(modes)} modes in router.")

    def level_2_swyh_bridge_presence(self) -> DiagnosticResult:
        """Verifies if the SWYH-RS bridge is exposed and has state tracking."""
        import src.core.main as main
        if not hasattr(main, 'toggle_swyh_rs'):
            return DiagnosticResult(2, "SWYH Bridge", "FAIL", "toggle_swyh_rs not found in main.py")
        if not hasattr(main, '_swyh_rs_process'):
            return DiagnosticResult(2, "SWYH Bridge", "FAIL", "_swyh_rs_process tracker not found in main.py")
        return DiagnosticResult(2, "SWYH Bridge", "PASS", "SWYH-RS bridge and state tracker found.")

    def level_3_batch_extract_presence(self) -> DiagnosticResult:
        """Verifies if the MKV batch extraction API is exposed."""
        import src.core.main as main
        if not hasattr(main, 'mkv_batch_extract'):
            return DiagnosticResult(3, "Batch Extract API", "FAIL", "mkv_batch_extract not found in main.py")
        return DiagnosticResult(3, "Batch Extract API", "PASS", "MKV batch extraction API confirmed.")

    def level_4_mpv_native_bridge(self) -> DiagnosticResult:
        """Verifies if the native MPV bridge is exposed."""
        import src.core.main as main
        if not hasattr(main, 'open_mpv'):
            return DiagnosticResult(4, "MPV Bridge", "FAIL", "open_mpv not found in main.py")
        return DiagnosticResult(4, "MPV Bridge", "PASS", "MPV native bridge confirmed.")

if __name__ == "__main__":
    AdvancedPlayerSuite().run()
