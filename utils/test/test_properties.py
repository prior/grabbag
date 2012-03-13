import unittest
from .. import properties

class PropertyTest(unittest.TestCase):

    def setUp(self): pass
    def tearDown(self): pass

    def test_lazy_property(self):

        class X(object):
            def __init__(self):
                self.calculation_count = 0
            @properties.lazy_property
            def expensive_value(self):
                self.calculation_count += 1
                return True

        x = X()
        self.assertEquals(0, x.calculation_count)
        self.assertTrue(x.expensive_value)
        self.assertEquals(1, x.calculation_count)
        self.assertTrue(x.expensive_value)
        self.assertEquals(1, x.calculation_count)

