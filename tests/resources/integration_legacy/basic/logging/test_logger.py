import unittest
import src.core.logger as logger

class TestLogger(unittest.TestCase):
    def test_set_debug_flags(self):
        flags = {'debug': True}
        logger.set_debug_flags(flags)
        # No exception should be raised

    def test_ui_handler_emit(self):
        handler = logger.UIHandler()
        record = logger.logging.LogRecord(
            name="test",
            level=logger.logging.INFO,
            pathname="",
            lineno=1,
            msg="Test message",
            args=(),
            exc_info=None
        )
        handler.emit(record)
        self.assertTrue(len(logger.LOG_BUFFER) > 0)

if __name__ == '__main__':
    unittest.main()
