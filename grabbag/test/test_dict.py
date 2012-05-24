import unittest
from ..dict import merge,mpop,mget

class DictTest(unittest.TestCase):

    def setUp(self): pass
    def tearDown(self): pass

    def test_merge(self):
        x = {'x':1}
        y = {'y':2}
        z = {'z':3}
        q = {'y':4}
        self.assertEquals({'x':1}, merge({},x))
        self.assertEquals({'x':1,'y':2,'z':3}, merge({},x,y,z))
        self.assertEquals({'x':1},x)
        self.assertEquals({'y':2},y)
        self.assertEquals({'z':3},z)
        self.assertEquals({'x':1,'y':4,'z':3}, merge({},x,y,z,q))
        self.assertEquals({'x':1},x)
        self.assertEquals({'y':2},y)
        self.assertEquals({'z':3},z)
        self.assertEquals({'x':1,'y':4,'z':3}, merge(x,y,z,q))
        self.assertEquals({'x':1,'y':4,'z':3},x)
        self.assertEquals({'y':2},y)
        self.assertEquals({'z':3},z)

    def test_mget(self):
        d = {'x':None, 'y':0}
        self.assertEquals(0,mget(d,'x','y'))
        self.assertEquals({'x':None, 'y':0},d)
        self.assertIsNone(mget(d,'z','q'))
        self.assertEquals(-1,mget(d,'z','q',fallback=-1))
        self.assertEquals({'x':None, 'y':0},d)

    def test_mpop(self):
        d = {'x':None, 'y':0}
        self.assertEquals(0, mpop(d,'x','y'))
        self.assertEquals({'x':None}, d)
        self.assertIsNone(mpop(d,'z','q'))
        self.assertEquals(-1, mpop(d,'z','q',fallback=-1))
        self.assertEquals({'x':None}, d)
       

