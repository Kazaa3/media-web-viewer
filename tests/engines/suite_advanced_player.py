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

    def level_5_handbrake_batch_engine(self) -> DiagnosticResult:
        """Verifies the TranscoderManager's batch processing capability."""
        from src.core.transcoder import TranscoderManager
        tm = TranscoderManager()
        task_ids = tm.add_batch_tasks([{"input": "in.mp4", "output": "out.mp4"}], {"preset": "fast"})
        if len(task_ids) == 1:
            return DiagnosticResult(5, "HandBrake Batch", "PASS", "Batch task queuing confirmed.")
        return DiagnosticResult(5, "HandBrake Batch", "FAIL", "Batch task queuing failed.")

    def level_6_external_players_presence(self) -> DiagnosticResult:
        """Checks for presence of critical external player binaries."""
        import shutil
        missing = []
        # swyh-rs-cli is now a priority requirement for advanced streaming
        for bin in ["vlc", "HandBrakeCLI", "mkvextract", "swyh-rs-cli"]:
            if not shutil.which(bin):
                missing.append(bin)
        
        # mpv is optional but recommended
        mpv_exists = shutil.which("mpv")
        
        if not missing:
            msg = "Critical tools found."
            if not mpv_exists: msg += " (Note: mpv not found, skipping native MPV tests)"
            return DiagnosticResult(6, "External Binaries", "PASS", msg)
        return DiagnosticResult(6, "External Binaries", "WARN", f"Missing binaries: {missing}")

    def level_7_library_presence(self) -> DiagnosticResult:
        """Verifies if the new toolchain libraries are importable."""
        missing = []
        try:
            import enzyme
        except ImportError:
            missing.append("enzyme")
        try:
            import pymkv
        except ImportError:
            missing.append("pymkv")
        try:
            import ffmpeg
        except ImportError:
            missing.append("ffmpeg-python")
            
        if not missing:
            return DiagnosticResult(7, "Library Presence", "PASS", "All toolchain libraries present.")
        return DiagnosticResult(7, "Library Presence", "FAIL", f"Missing libraries: {missing}")

if __name__ == "__main__":
    AdvancedPlayerSuite().run()
