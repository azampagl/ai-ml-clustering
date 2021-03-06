"""
"""
class dotdict(dict):
    """
    Extends normal dictionary for dot evaluations.
    """
    def __getattr__(self, attr):
        return self.get(attr, None)
    __setattr__= dict.__setitem__
    __delattr__= dict.__delitem__