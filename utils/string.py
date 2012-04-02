def nstrip(s): return None if s is None else s.strip()
def nlower(s): return None if s is None else s.lower()
def nupper(s): return None if s is None else s.upper()

def cutoff(s, amt): return s if len(s or '') <= amt else "%s..."%s[0:amt-3]
