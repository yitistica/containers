from containers.core.base import BaseSequence, BaseSet, BaseFrozenSet
from containers.collections.elementary.common import ElementView


class InvalidCategoryValueError(Exception):
    def __init__(self, value, category):
        message = f'Given value {value} is not of part of <{category}> .'
        super().__init__(message)


class CategorySequence(BaseSequence):
    """
    """
    def __init__(self, categories):

        super().__init__()

    def _set_item(self, index, value):

        self._list[index] = value


class RecursiveIterView(object):

    def __init__(self, iterable, from_=None, to_=None, step=1, max_loop=None, max_step=None):
        self._iterable = iterable
        self._size = len(self._iterable)

        self._from, self._to = self._parse_range(from_=from_, to_=to_)

        self._current_step = 0
        self._current_loop = 0
        self._max_step = max_step
        self._max_loop = max_loop

    def _parse_range(self, from_, to_):
        if not from_:
            from_ = 0

        if not to_:
            to_ = self._size

        if from_ < 0:
            from_ = self._size + from_

        if to_ < 0:
            to_ = self._size + to_

        return from_, to_

    def __iter__(self):
        return self

    def __next__(self):
        self.current += 1
        if self.current < self.high:
            return self.current
        raise StopIteration




class StatisticsView(object):
    pass

    def apply(self):
        pass

    def count(self):
        pass


class SetView(object):
    def __init__(self, iterable):
        BaseSet(iterable)


class MapView(object):
    pass


class LocationView(object):

    def __getitem__(self, item):
        # apply a function;
        pass


class RandomView(object):
    pass


class XList(BaseSequence):

    def repeat(self, from_=None, to_=None):
        return None


a = RecursiveIterView(list([1,2,3,4,5,6]), to_=-1)

print(a._to)
