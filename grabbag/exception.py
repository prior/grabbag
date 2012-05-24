from .list import first_not_none
import sys

# allows wrapping of another error or not-- a good class to use as your base for your own exception tree
class Error(Exception):
    def __init__(self, msg=None, err=None):
        super(Error, self).__init__(msg or err and unicode(err) or '')
        self.msg = msg or ''
        self.err = err

    @property
    def wrapped_error_str(self):
        if not self.err: return ''
        return u'[%s:%s]' % (self.err.__class__.__name__, self.err)

    def __str__(self): return unicode(self).encode('utf-8')
    def __unicode__(self):
        return u'%s%s' % (self.msg, self.wrapped_error_str)
    def __repr__(self):
        return '%s(%s,%s)' % (self.__class__.__name__, repr(self.msg), repr(self.err))

    # raises wrapped exception appropriately or normal excpetion normally
    def _raise(self):
        if self.err:
            raise self, None, sys.exc_info()[2]
        raise self

