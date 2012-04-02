import unittest
from .. import property

class PropertyTest(unittest.TestCase):

    def setUp(self): pass
    def tearDown(self): pass

    def test_cached_property(self):

        class X(object):
            def __init__(self):
                super(X, self).__init__()
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

    def test_dynamic_cached_property(self):
        class X(object):
            def __init__(self):
                super(X, self).__init__()

            @classmethod
            def create_caching(kls):
                @property.cached_property
                def _tmp(self):
                    print "bye"
                kls.yox = _tmp

        def _tmp(self):
            print "hello"
            return 1

        #X.yo = _tmp
        #property.cached_property(X.yo)
        #X.blah = property.cached_property
        #X.blah(_tmp,attr='yo')
#        X.blah(X.yo)
        X.yo = property.cached_property(_tmp)
        x = X()
        from pprint import pprint
        pprint(x.__dict__)
        print x.yo
        pprint(x.__dict__)
        print x.yo
        print x.yo
#        x._tmp
        #X.create_caching()
        #x = X()
        #x.yox()
        #x.yox()
        #x.yox()


    #def test_descriptor(self):
        #class Descriptor(self,f)
