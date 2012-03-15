from .list import first_not_none


def merge(destination, source):
    destination.update(source)
    return destination

def mpop(d, *args, **kwargs):
    val = first_not_none((d.pop(a,None) for a in args))
    if val is not None: return val
    return kwargs.get('fallback',None)

def mget(d, *args, **kwargs):
    val = first_not_none((d.get(a,None) for a in args))
    if val is not None: return val
    return kwargs.get('fallback',None)
