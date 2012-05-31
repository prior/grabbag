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

# i.e. an iterable that is not a string: from http://stackoverflow.com/questions/1835018/python-check-if-an-object-is-a-list-or-tuple-but-not-string
def is_sequence(arg): 
    return (not hasattr(arg, "strip") and hasattr(arg, "__getitem__") or hasattr(arg, "__iter__"))
