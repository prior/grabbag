import unittest
from ..exception import Error

class DomainError(Error): pass

class ErrorTest(unittest.TestCase):

    def setUp(self): pass
    def tearDown(self): pass

    def test_representations(self):
        literal = u"blah \u2603"
        err = DomainError(literal)
        self.assertEquals(literal, unicode(err))
        self.assertEquals(unicode(literal).encode('utf-8'), str(err))
        self.assertEquals('DomainError(%s,None)'%repr(literal), repr(err))

        err = DomainError("domain "+literal, ValueError(literal))
        self.assertEquals("domain %s[ValueError:%s]"%(literal,literal), unicode(err))

    def test_raise(self):
        with self.assertRaises(DomainError):
            DomainError()._raise()

        with self.assertRaises(DomainError):
            DomainError("outside", ValueError("inside"))._raise()

    def test_everything(self):
        in_appropriate_except_clause = False
        try:
            try:
                raise ValueError(u"inner msg")
            except ValueError as err:
                DomainError(u"outer msg", err)._raise()
        except DomainError as err:
            in_appropriate_except_clause = True
            self.assertEquals(ValueError, err.err.__class__)
            self.assertEquals(u"inner msg", unicode(err.err))
            self.assertEquals(u"outer msg", err.msg)
        self.assertTrue(in_appropriate_except_clause)



    # this test needs human visual inspection, so it is not run by default -- unskip to force a run
    # haven't spent time to figure out how to do programmatically -- just checking that raising a wrapped excpetion also includes the stack trace from that exception
    @unittest.skip
    def test_good_stacktrace(self):
        def bar(): raise ValueError(u"inner msg")
        def foo(): return bar()
        def baz(err): DomainError(u"outer msg", err)._raise()

        try:
            foo()
        except ValueError as err:
            baz(err)

    # this just confirms what happens when you don't do the appropriate raise
    @unittest.skip
    def test_bad_stacktrace(self):
        def bar(): raise ValueError(u"inner msg")
        def foo(): return bar()
        def baz(err): raise DomainError(u"outer msg", err)

        try:
            foo()
        except ValueError as err:
            baz(err)
