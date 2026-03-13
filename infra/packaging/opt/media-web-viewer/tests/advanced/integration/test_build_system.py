import unittest
from infra.build_system import BuildSystem

class TestBuildSystem(unittest.TestCase):
    def setUp(self):
        self.bs = BuildSystem()

    def test_read_version(self):
        version = self.bs._read_version()
        self.assertIsInstance(version, str)

    def test_print_banner(self):
        # Should print banner without error
        self.bs._print_banner("Test Banner")

    def test_check_environment(self):
        result = self.bs.check_environment()
        self.assertIsInstance(result, bool)

    def test_check_browser_available(self):
        result = self.bs._check_browser_available()
        self.assertIsInstance(result, bool)

if __name__ == '__main__':
    unittest.main()
