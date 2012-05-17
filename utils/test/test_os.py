import unittest
import os
from ..os import get_pid, get_parent_pid, get_grandparent_pid

class OSTest(unittest.TestCase):

    def setUp(self): pass
    def tearDown(self): pass

    def test_current_process_ancestry(self):
        self.assertEquals(os.getpid(), get_pid())
        self.assertEquals(os.getppid(), get_parent_pid())
        self.assertEquals(os.getppid(), get_parent_pid(get_pid()))
        self.assertEquals(get_parent_pid(get_parent_pid(get_pid())), get_grandparent_pid())
        self.assertEquals(0, get_parent_pid(1))
        self.assertEquals(0, get_parent_pid(0))
        self.assertEquals(0, get_grandparent_pid(0))
        self.assertEquals(0, get_grandparent_pid(1))
