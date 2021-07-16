

class Key(object):
    def __init__(self, index, key):
        self._index = index
        self._key = key

    def __hash__(self):
        return self._index

    def __repr__(self):
        return repr(self._key)


class Value(object):
    def __init__(self, value):
        self._value = value

    def __repr__(self):
        return repr(self._value)


class Mapping(object):
    def __init__(self, index , key_object, value):
        pass


a = {Key(index=1, key=2) : Value(2)}

print(a[1:2])