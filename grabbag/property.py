CACHED_PREFIX = '_cached_'

class cached_property(object):
    def __init__(self, f, name=None, *fargs):
        super(cached_property, self).__init__()
        self.f = f
        self.fargs = fargs
        self.attr = '%s%s' % (CACHED_PREFIX, name or f.__name__)

    def __get__(self, obj, type=None):
        if not hasattr(obj, self.attr):
            setattr(obj, self.attr, self.f(obj, *self.fargs))
        return getattr(obj, self.attr)

    def __set__(self, obj, value):
        setattr(obj, self.attr, value)

    def __delete__(self, obj):
        if hasattr(obj, self.attr):
            delattr(obj, self.attr)

# so you don't have to remember what variables are stored as, and you have a way to see if caching happened without triggering the actual evaluation
def is_cached(obj, attr): return hasattr(obj, cached_key(attr))
def cached_value(obj, attr, default=None): return getattr(obj, cached_key(attr), default)
def cached_key(attr): return '%s%s' % (CACHED_PREFIX, attr)
def delete_cache(obj, *attrs): 
    for attr in attrs: 
        if is_cached(obj,attr): 
            delattr(obj, cached_key(attr))


# for backward compatability
lazy_property = cached_property
