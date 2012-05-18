import unittest
import os, shutil
from ..os import FileLock, get_pid, get_parent_pid, get_grandparent_pid

TEST_LOCK_PLAYGROUND = 'lock_playground'

class OSTest(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_LOCK_PLAYGROUND): 
            self.tearDown()
        os.mkdir(TEST_LOCK_PLAYGROUND)

    def tearDown(self):
        shutil.rmtree(TEST_LOCK_PLAYGROUND)

    def test_current_process_ancestry(self):
        self.assertEquals(os.getpid(), get_pid())
        self.assertEquals(os.getppid(), get_parent_pid())
        self.assertEquals(os.getppid(), get_parent_pid(get_pid()))
        self.assertEquals(get_parent_pid(get_parent_pid(get_pid())), get_grandparent_pid())
        self.assertEquals(0, get_parent_pid(1))
        self.assertEquals(0, get_parent_pid(0))
        self.assertEquals(0, get_grandparent_pid(0))
        self.assertEquals(0, get_grandparent_pid(1))

    def setUp(self):
        if os.path.exists(TEST_LOCK_PLAYGROUND): 
            self.tearDown()
        os.mkdir(TEST_LOCK_PLAYGROUND)

    def tearDown(self):
        shutil.rmtree(TEST_LOCK_PLAYGROUND)

    def test_basic_lock(self):
        fl = FileLock('%s/main'%TEST_LOCK_PLAYGROUND)
        self.assertFalse(os.path.exists(fl.lock_dir))
        self.assertFalse(fl.locked)
        self.assertTrue(fl.lock())
        self.assertTrue(fl.locked)
        self.assertTrue(os.path.exists(fl.lock_dir))
        self.assertTrue(fl.unlock())
        self.assertFalse(fl.locked)
        self.assertFalse(os.path.exists(fl.lock_dir))

    def test_lock_block(self):
        fl1 = FileLock('%s/block'%TEST_LOCK_PLAYGROUND, 0, 0)
        fl2 = FileLock('%s/block'%TEST_LOCK_PLAYGROUND, 0, 0)
        self.assertTrue(fl1.lock())
        self.assertFalse(fl2.lock())
        self.assertTrue(fl1.unlock())
        self.assertTrue(fl2.lock())
        self.assertFalse(fl1.lock())
        self.assertTrue(fl2.unlock())

    def test_with(self):
        fl = FileLock('%s/shared'%TEST_LOCK_PLAYGROUND, 0, 0)
        self.assertFalse(os.path.exists(fl.lock_dir))
        self.assertFalse(fl.locked)
        with fl:
            self.assertTrue(os.path.exists(fl.lock_dir))
            self.assertTrue(fl.locked)
        self.assertFalse(os.path.exists(fl.lock_dir))
        self.assertFalse(fl.locked)


