from models import Entry as DBDictEntry

class DBDictUnsupportedType(Exception): pass

class DBDict:
    """A dictionary which stores data in the database"""
    def __init__(self, name):
        self.qs = DBDictEntry.objects
        self.name = name
        
    def __getitem__(self, key):
        key_hash, key = self.helpers.make_key(key)
        entry = self._get_entry(key_hash)
        if not entry:
            raise KeyError(key)
        return eval(entry.data)
    
    def __setitem__(self, key, data):
        try: hash(data)
        except TypeError: raise DBDictUnsupportedType(data)
        key_hash, key = self.helpers.make_key(key)
        entry = self._get_entry(key_hash) or DBDictEntry(name=self.name, key_hash=key_hash, key=key)
        entry.data = repr(data)        
        entry.save()
    
    def __delitem(self, key):
        key_hash = self.helpers.make_key(key)[0]
        self.qs.filter(name=self.name, key=key_hash).delete()
    
    def __contains__(self, key):
        key_hash = self.helpers.make_key(key)[0]
        return 0 < self.qs.filter(name=self.name, key_hash=key_hash).count()
    
    def get(self, key, default=None):
        key_hash = self.helpers.make_key(key)[0]
        return self._get_entry(key_hash, default=default)
    
    def setdefault(self, key, default=None):
        try: hash(data)
        except TypeError: raise DBDictUnsupportedType(data)
        key_hash, key = self.helpers.make_key(key)
        entry, created = self.qs.get_or_create(name=self.name, key_hash=key_hash, key=key,
                                              defaults={'data': repr(default)})
        return eval(entry.data)

    def __repr__(self):
        return 'DBDict(%s)' % repr(self.name)
    
    def __str__(self):
        return repr(self)

    def _get_entry(self, key_hash, default=None):
        try:
            return self.qs.get(name=self.name, key_hash=key_hash)
        except DBDictEntry.DoesNotExist, e:
            return default
    
    def iterkeys(self):
        for i in self.qs.filter(name=self.name).values_list('key', flat=True):
            yield eval(i)
    
    def iteritems(self):
        for i in self.qs.filter(name=self.name).values_list('key', 'data'):
            yield tuple(map(eval, i))
    
    def itervalues(self):
        for i in self.qs.filter(name=self.name).values_list('data', flat=True):
            yield eval(i)
    
    def keys(self): return list(self.iterkeys)
    def items(self): return list(self.iteritems)
    def values(self): return list(self.itervalues)
    
    class helpers:
        @staticmethod
        def make_key(key):
            return (hash(key), repr(key))

