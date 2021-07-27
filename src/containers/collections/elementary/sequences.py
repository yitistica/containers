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


class IterView(object):

    def __init__(self, iterable, from_=None, to_=None, step=1, max_loop=1, max_step=None, restart=False):
        self._iterable = iterable
        self._size = None  # subset size;

        self._from, self._to, self._step = self._parse_range(from_=from_, to_=to_, step=step)

        self._current_step = 0
        self._current_loop = 0
        self._max_step = max_step
        self._max_loop = max_loop

    def _parse_range(self, from_, to_, step):

        _iterable_size = len(self._iterable)

        if not from_:
            from_ = 0
        elif (-_iterable_size) <= from_ < 0:
            from_ = _iterable_size + from_
        else:
            raise IndexError(f"index {from_} out of range")

        if not to_:
            to_ = _iterable_size
        elif (-_iterable_size) <= to_ < 0:
            to_ = _iterable_size + to_
        else:
            raise IndexError(f"index {from_} out of range")

        if not step:
            step = 1

        assert isinstance(from_, int)
        assert isinstance(to_, int)
        assert isinstance(step, int)

        if from_ > to_:
            raise ValueError(f"from_ position is greater than to_ position, "
                             f"use step < 0 to set reverse order.")
        else:
            self._size = to_ - from_

        return from_, to_, step

    def __iter__(self):
        return self

    def __next__(self):

        if self._max_step and (self._current_step >= self._max_step):
            raise StopIteration

        if self._max_loop and (self._current_loop >= self._max_loop):
            raise StopIteration

        # self._current_step //

        raise StopIteration

        return


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


# a = IterView(list([1, 2, 3, 4, 5, 6]), to_=-1)

a = [1,2,3, 4, 5]

print(a[0:1])




