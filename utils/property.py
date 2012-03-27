class cached_property(object):
    def __init__(self, f):
        super(cached_property, self).__init__()
        self.f = f
        self.attr = '_cached_%s' % f.__name__

    def __get__(self, obj, type=None):
        if not hasattr(obj, self.attr):
            setattr(obj, self.attr, self.f(obj))
        return getattr(obj, self.attr)

    def __set__(self, obj, value):
        setattr(obj, self.attr, value)

    def __delete__(self, obj):
        if hasattr(obj, self.attr):
            delattr(obj, self.attr)

# for backward compatability
lazy_property = cached_property
