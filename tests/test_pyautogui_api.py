import sys
sys.path.insert(0, '..')  # Ensure main.py and dependencies are importable

import unittest

class TestPyAutoGuiAPI(unittest.TestCase):
    def test_pyautogui_api(self):
        import main
        result = main.test_pyautogui()
        self.assertIn('status', result)
        self.assertEqual(result['status'], 'ok')
        self.assertIn('screen_size', result)
        self.assertIn('mouse_position', result)
        self.assertIsInstance(result['screen_size'], dict)
        self.assertIsInstance(result['mouse_position'], dict)
        self.assertIn('width', result['screen_size'])
        self.assertIn('height', result['screen_size'])
        self.assertIn('x', result['mouse_position'])
        self.assertIn('y', result['mouse_position'])

if __name__ == '__main__':
    unittest.main()
