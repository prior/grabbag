from .property import is_cached

def kwargs_str(obj, attrs=None, cached=None):
    ktuples = [(k,repr(getattr(obj,k))) for k in (attrs or []) if hasattr(obj,k)]
    ktuples += [(k,repr(getattr(obj,k))) for k in (cached or []) if is_cached(obj,k)]
    return ','.join(['%s=%s'%t for t in ktuples])

def from_obj(obj, obj_attrs=None, *attrs):
    d = dict((a,getattr(obj,a)) for a in attrs if obj.hasattr(obj,a))
    for a in obj_attrs: 
        if obj.hasattr(a):
            d.update(from_obj(getattr(obj,a)))
    return d

def mgetattr(obj, attrs, *args): return tuple([getattr(obj, a, *args) for a in attrs])
    

