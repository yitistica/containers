"""

difference: mutability, uniqueness, order,
"""

_ITERABLE_ATTR_NAMES = ['_iterable', 'iterable', '_list']


def _check_contain_iterable(self, iterable_attr_name):
    return hasattr(self, iterable_attr_name)


class IterBase(object):
    _iterable_attr_name = '_iterable'

    def __init__(self):
        assert _check_contain_iterable(self, iterable_attr_name=self._iterable_attr_name)

    @property
    def iterable(self):
        return getattr(self, self._iterable_attr_name)

    def __iter__(self):
        return self

