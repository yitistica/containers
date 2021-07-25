
class Element(object):
    def __init__(self, value):
        self._set(value)

    def _set(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    def __str__(self):
        return str(self._value)

    def __repr__(self):
        return repr(self._value)


class Key(Element):
    pass


class ImmutableKey(Key):
    def __init__(self, value):
        hash(value)
        super().__init__(value=value)

    def __hash__(self):
        return hash(self._value)


class StrKey(ImmutableKey):
    def __init__(self, value):
        if not isinstance(value, str):
            raise TypeError(f'{value} is not a str.')
        super().__init__(value)


class Value(Element):
    pass


class ItemKeyTypeError(Exception):
    def __init__(self, key_value):
        message = f'Given key is of the type <{type(key_value)}> .'
        super().__init__(message)


class ItemValueTypeError(Exception):
    def __init__(self, value):
        message = f'Given value is of the type <{type(value)}> .'
        super().__init__(message)


class Item(object):
    def __init__(self, key, value):
        self._set_key(key=key)
        self._set_value(value=value)

    def _set_key(self, key):
        if not isinstance(key, Key):
            raise ItemKeyTypeError(key)

        self._key = key

    def _set_value(self, value):
        if not isinstance(value, Value):
            raise ItemValueTypeError(value)

        self._value = value

    def _get_key(self):
        return self._key

    def _get_value(self):
        return self._value

    @property
    def key(self):
        return self._get_key()

    @property
    def value(self):
        return self._get_value()

