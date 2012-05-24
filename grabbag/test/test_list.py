import unittest
from ..list import first_not_none

class ListTest(unittest.TestCase):

    def setUp(self): pass
    def tearDown(self): pass

    def test_first_not_none(self):
        self.assertEquals(3,first_not_none((None,None,3)))
        self.assertEquals(3,first_not_none((None,None,3),4))
        self.assertIsNone(first_not_none((None,None)))
        self.assertEquals(4,first_not_none((None,None),4))
        self.assertEquals(4,first_not_none((None,None),4))
        self.assertEquals(5,first_not_none((5,4,3)))

        #generators
        self.assertIsNone(first_not_none((None for i in xrange(100))))
        self.assertEquals(-1,first_not_none((None for i in xrange(100)),-1))
        self.assertEquals(-1,first_not_none((i>=99 and -1 or None for i in xrange(100))))


