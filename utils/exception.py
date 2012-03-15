import sys

def reraise(err):
    raise err, None, sys.exc_info()[2]

class WrappedError(ValueError):
    def __init__(self, info=None, err=None):
        super(WrappedError, self).__init__(str(info or err))
        self.wrapped_error = err
        self.extra_info = info

    @property
    def wrapped_error_str(self):
        if self.wrapped_error:
            return '[ %s: %s ]' % (str(self.wrapped_error.__class__).split("'")[1],str(self.wrapped_error))
        return None

    def __str__(self):
        return ('%s %s' % (self.extra_info, self.wrapped_error_str or '')).strip()

