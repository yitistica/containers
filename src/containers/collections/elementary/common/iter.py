

_ITERABLE_ATTR_NAMES = ['_iterable', 'iterable', '_list']


def _check_contain_iterable(self):
    contained = False

    for attr_name in _ITERABLE_ATTR_NAMES:
        if hasattr(self, attr_name):
            return attr_name

    if not contained:
        raise AttributeError(f"obj {self} does not contain an iterable "
                             f"as an attribute named one of {_ITERABLE_ATTR_NAMES}.")


class IterBase(object):

    def __init__(self):
        self.__iterable = _check_contain_iterable(self)

