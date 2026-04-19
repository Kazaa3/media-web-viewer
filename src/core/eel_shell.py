import logging
import sys

log = logging.getLogger("eel_shell")

class EelFallback:
    """
    Mock Eel implementation to prevent import-time crashes and provide 
    diagnostic feedback when the 'eel' package is missing (v1.46.140).
    """
    def __init__(self):
        self._is_mock = True
        self._exposed = []

    def expose(self, func):
        """Mock decorator for @eel.expose"""
        self._exposed.append(func.__name__)
        return func

    def init(self, *args, **kwargs):
        log.warning("[EelShell] Mock init() called. UI will not render.")

    def start(self, *args, **kwargs):
        log.critical("[EelShell] Mock start() called! The 'eel' package is missing from this environment.")
        log.info(f"Python Executable: {sys.executable}")
        log.info(f"Python Path: {sys.path}")
        sys.exit(1)

    def sleep(self, seconds):
        import time
        time.sleep(seconds)

    def __getattr__(self, name):
        # Fallback for any other eel calls
        def dummy(*args, **kwargs):
            log.error(f"[EelShell] Undefined call: eel.{name}()")
            return None
        return dummy

# Try to import real eel, fallback to mock if missing
try:
    import eel as real_eel
    eel = real_eel
    log.debug("[EelShell] Real 'eel' package imported successfully.")
except ImportError:
    log.warning("[EelShell] 'eel' package not found. Using Mock Fallback.")
    eel = EelFallback()
