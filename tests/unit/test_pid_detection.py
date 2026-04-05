import sys
import os
import unittest
from unittest.mock import patch, MagicMock
from collections import namedtuple

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/core')))

# Mock psutil before importing main if possible, but main does its own imports
# So we mock it at the module level in main.py during the test

from src.core.main import check_running_sessions

class TestPIDDetection(unittest.TestCase):
    @patch('psutil.net_connections')
    @patch('psutil.process_iter')
    @patch('os.getpid')
    def test_check_running_sessions_finds_match(self, mock_getpid, mock_process_iter, mock_net_conn):
        mock_getpid.return_value = 1000
        
        # Mock connection
        Addr = namedtuple('Addr', ['ip', 'port'])
        Conn = namedtuple('Conn', ['status', 'pid', 'laddr'])
        mock_net_conn.return_value = [
            Conn(status='LISTEN', pid=2000, laddr=Addr(ip='127.0.0.1', port=8001))
        ]
        
        # Mock process
        ProcessInfo = namedtuple('ProcessInfo', ['info'])
        mock_process_iter.return_value = [
            ProcessInfo(info={'pid': 2000, 'name': 'python', 'cmdline': ['python', 'src/core/main.py']})
        ]
        
        sessions = check_running_sessions()
        
        self.assertEqual(len(sessions), 1)
        self.assertEqual(sessions[0]['pid'], 2000)
        self.assertEqual(sessions[0]['port'], 8001)
        self.assertIn('main.py', sessions[0]['cmdline'])

    @patch('psutil.net_connections')
    @patch('psutil.process_iter')
    @patch('os.getpid')
    def test_check_running_sessions_ignores_current(self, mock_getpid, mock_process_iter, mock_net_conn):
        mock_getpid.return_value = 1000
        
        mock_net_conn.return_value = []
        
        ProcessInfo = namedtuple('ProcessInfo', ['info'])
        mock_process_iter.return_value = [
            ProcessInfo(info={'pid': 1000, 'name': 'python', 'cmdline': ['python', 'src/core/main.py']})
        ]
        
        sessions = check_running_sessions()
        self.assertEqual(len(sessions), 0)

if __name__ == '__main__':
    unittest.main()
