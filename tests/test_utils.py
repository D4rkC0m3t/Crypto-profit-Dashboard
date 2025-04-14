import sys
import os
import unittest

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from utils import format_large_number

class TestUtils(unittest.TestCase):
    def test_format_large_number(self):
        """Test the format_large_number function"""
        self.assertEqual(format_large_number(1000), "1.00K")
        self.assertEqual(format_large_number(1500), "1.50K")
        self.assertEqual(format_large_number(1000000), "1.00M")
        self.assertEqual(format_large_number(1500000), "1.50M")
        self.assertEqual(format_large_number(1000000000), "1.00B")
        self.assertEqual(format_large_number(1500000000), "1.50B")
        self.assertEqual(format_large_number(123), "123.00")

if __name__ == '__main__':
    unittest.main()
