# specifically chose not to use *args here cuz that unnecessarily unwinds generator expressions
def first_not_none(iterable, fallback=None):
    """ return the first item that is not None """
    for obj in iterable:
        if obj is not None: return obj
    return fallback

# specifically chose not to use *args here cuz that unnecessarily unwinds generator expressions
def first_truthy(iterable, fallback=None):
    """ return the first item that is truth """
    for obj in iterable:
        if obj: return obj
    return fallback

def sort(obj, *args, **kwargs):
    """ a sort that actually returns the object being sorted """
    obj.sort(*args, **kwargs)
    return obj


