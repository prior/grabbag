def first_not_none(list_, fallback=None):
    """ return the first item that is not None """
    for l in list_:
        if l is not None: return l
    return fallback

def first_truthy(list_, fallback=None):
    """ return the first item that is truth """
    for l in list_:
        if l:  return l
    return fallback

def sort(obj, *args, **kwargs):
    """ a sort that actually returns the object being sorted """
    obj.sort(*args, **kwargs)
    return obj


