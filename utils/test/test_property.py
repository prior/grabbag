import unittest
from .. import property

class PropertyTest(unittest.TestCase):

    def setUp(self): pass
    def tearDown(self): pass

    def test_cached_property(self):

        class X(object):
            def __init__(self):
                self.calculation_count = 0
            @property.cached_property
            def expensive_value(self):
                self.calculation_count += 1
                return True

        x = X()
        self.assertEquals(0, x.calculation_count)
        self.assertTrue(x.expensive_value)
        self.assertEquals(1, x.calculation_count)
        self.assertTrue(x.expensive_value)
        self.assertEquals(1, x.calculation_count)
        del x.expensive_value
        self.assertTrue(x.expensive_value)
        self.assertEquals(2, x.calculation_count)
        x.expensive_value = False
        self.assertFalse(x.expensive_value)
        self.assertEquals(2, x.calculation_count)

