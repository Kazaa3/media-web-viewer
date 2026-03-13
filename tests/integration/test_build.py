import unittest
import build

class TestBuild(unittest.TestCase):
    def test_run_build_test_gate(self):
        # Should not raise exception
        try:
            build.run_build_test_gate()
        except Exception:
            self.fail("run_build_test_gate() raised Exception unexpectedly!")

if __name__ == '__main__':
    unittest.main()
