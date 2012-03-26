import unittest
from .. import dict as d

class DictTest(unittest.TestCase):

    def setUp(self): pass
    def tearDown(self): pass

    def test_merge(self):
        x = {'x':1}
        y = {'y':2}
        z = {'z':3}
        q = {'y':4}
        self.assertEquals({'x':1}, d.merge({},x))
        self.assertEquals({'x':1,'y':2,'z':3}, d.merge({},x,y,z))
        self.assertEquals({'x':1},x)
        self.assertEquals({'y':2},y)
        self.assertEquals({'z':3},z)
        self.assertEquals({'x':1,'y':4,'z':3}, d.merge({},x,y,z,q))
        self.assertEquals({'x':1},x)
        self.assertEquals({'y':2},y)
        self.assertEquals({'z':3},z)
        self.assertEquals({'x':1,'y':4,'z':3}, d.merge(x,y,z,q))
        self.assertEquals({'x':1,'y':4,'z':3},x)
        self.assertEquals({'y':2},y)
        self.assertEquals({'z':3},z)

