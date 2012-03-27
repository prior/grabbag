def merge(destination, *sources):
    if isinstance(sources, dict): sources = [sources]
    for source in sources:
        destination.update(source)
    return destination

def mpop(d, *args, **kwargs):
    for a in args:
        if d.get(a) is not None: return d.pop(a)
    return kwargs.get('fallback',None)

def mget(d, *args, **kwargs):
    for a in args:
        if d.get(a) is not None: return d.get(a)
    return kwargs.get('fallback',None)

