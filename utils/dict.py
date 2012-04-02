def merge(destination, *sources):
    if isinstance(sources, dict): sources = [sources]
    for source in sources:
        if source: destination.update(source)
    return destination

def mpop(d, *args, **kwargs):
    for a in args:
        if d.get(a) is not None: return d.pop(a)
    return kwargs.get('fallback',None)

def mget(d, *args, **kwargs):
    for a in args:
        if d.get(a) is not None: return d[a]
    return kwargs.get('fallback',None)

def getdict(d, *only_args):
    return dict((k,v)for k,v in d.iteritems() if k in only_args)

def popdict(d, *only_args):
    subdict = getdict(d, *only_args)
    for k in subdict: d.pop(k)
    return subdict

def kwargs_str(d, *only_args):
    return ','.join(["%s=%s"%(k,repr(d[k])) for k in (only_args or d.keys())])

