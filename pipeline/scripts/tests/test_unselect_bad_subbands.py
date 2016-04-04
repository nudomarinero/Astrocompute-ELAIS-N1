from __future__ import print_function
import sys
import unittest
import traceback
import os

# Append the path of the module to the syspath
sys.path.append('..')
from unselect_subbands import unselect


class TestEvenFrequencies(unittest.TestCase):
    def setUp(self):
        self.list_dir1 = [(100, "file1"),
                          (100, "file2"),
                          ( 50, "file3")]
        self.list_dir2 = [(100, "file1"),
                          (100, "file2"),
                          ( 99, "file3")]
    
    def test_unselection1(self):
        self.assertEqual(unselect(self.list_dir1), ["file3"])
        
    def test_unselection2(self):
        self.assertEqual(unselect(self.list_dir2), ["file3"])
        
if __name__ == '__main__':
    unittest.main()