import unittest
from ..property import cached_property, is_cached, cached_value, delete_caches, freshen


class ObjectWithCachedValue(object):
    def __init__(self):
        super(ObjectWithCachedValue, self).__init__()
        self.calc_count = 0
        self.extra_val = True

    @cached_property
    def val(self):
        self.calc_count += 1
        return True

    @cached_property
    def extra(self):
        return self.extra_val


class PropertyTest(unittest.TestCase):
    def setUp(self): 
        self.obj = ObjectWithCachedValue()
    def tearDown(self): pass

    def test_cached_property_gets(self):
        self.assertIs(0, self.obj.calc_count)
        self.assertIs(True, self.obj.val)
        self.assertIs(1, self.obj.calc_count)
        self.assertIs(True, self.obj.val)
        self.assertIs(1, self.obj.calc_count)

    def test_cached_property_sets(self):
        self.assertIs(True, self.obj.val)
        self.assertIs(1, self.obj.calc_count)
        self.obj.val = False
        self.assertIs(False, self.obj.val)
        self.assertIs(1, self.obj.calc_count)

    def test_cached_property_dels(self):
        self.assertFalse(is_cached(self.obj, 'val'))
        del self.obj.val # just making sure we're ok del-ing non-existence values
        self.assertFalse(is_cached(self.obj, 'val'))
        self.assertIs(True, self.obj.val)
        self.assertIs(1, self.obj.calc_count)
        self.assertTrue(is_cached(self.obj, 'val'))
        del self.obj.val
        self.assertFalse(is_cached(self.obj, 'val'))
        self.assertIs(True, self.obj.val)
        self.assertIs(2, self.obj.calc_count)
        self.assertTrue(is_cached(self.obj, 'val'))

    def test_is_cached(self):
        self.assertFalse(is_cached(self.obj, 'val'))
        self.assertIs(True, self.obj.val)
        self.assertTrue(is_cached(self.obj, 'val'))
        self.obj.val = False
        self.assertTrue(is_cached(self.obj, 'val'))
        del self.obj.val
        self.assertFalse(is_cached(self.obj, 'val'))

    def test_cached_value(self):
        self.assertIsNone(cached_value(self.obj, 'val'))
        self.assertIs('default',cached_value(self.obj, 'val', 'default'))
        self.assertIs(True, self.obj.val)
        self.assertIs(True, cached_value(self.obj, 'val'))
        self.assertIs(True, cached_value(self.obj, 'val', 'default'))

    def test_delete_all(self):
        self.assertIs(True,self.obj.val)
        self.assertIs(True,self.obj.extra)
        self.assertTrue(is_cached(self.obj, 'val'))
        self.assertTrue(is_cached(self.obj, 'extra'))
        delete_caches(self.obj, 'val', 'extra')
        self.assertFalse(is_cached(self.obj, 'val'))
        self.assertFalse(is_cached(self.obj, 'extra'))
        self.assertIs(True,self.obj.val)
        self.assertTrue(is_cached(self.obj, 'val'))
        delete_caches(self.obj, 'val', 'extra') # make sure partial delete is ok
        self.assertFalse(is_cached(self.obj, 'val'))
        self.assertFalse(is_cached(self.obj, 'extra'))

    def test_freshen(self):
        self.assertIs(True, self.obj.extra)
        self.obj.extra_val = False
        self.assertIs(True, self.obj.extra)
        self.assertIs(False, freshen(self.obj, 'extra'))
        self.assertIs(False, self.obj.extra)
        self.obj.extra_val = True
        self.assertIs(False, self.obj.extra)
        self.assertIs(True, freshen(self.obj, 'extra'))
        self.assertIs(True ,self.obj.extra)

    ##TODO: Revisit and clean up 
    #def test_dynamic_cached_property(self):
        #class X(object):
            #def __init__(self):
                #super(X, self).__init__()

            #@classmethod
            #def create_caching(kls):
                #@cached_property
                #def _tmp(self):
                    #print "bye"
                #kls.yox = _tmp

        #def _tmp(self):
            #print "hello"
            #return 1

        #X.yo = cached_property(_tmp)
        #x = X()

