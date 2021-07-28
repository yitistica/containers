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

    def __init__(self, iterable, from_=None, to_=None, step=1, max_loop=1, max_step=None, restart_loop=False):
        self._iterable = iterable
        self._size = None  # subset size;

        self._from, self._to, self._step = self._parse_range(from_=from_, to_=to_, step=step)
        self._restart = restart_loop

        self._current_step = 0
        self._max_step = max_step
        self._max_loop = max_loop

    def _parse_range(self, from_, to_, step):

        _iterable_size = len(self._iterable)

        if from_ is None:
            from_ = 0
        elif 0 <= from_ < _iterable_size:
            pass
        elif (-_iterable_size) <= from_ < 0:
            from_ = _iterable_size + from_
        else:
            raise IndexError(f"index {from_} out of range")

        if to_ is None:
            to_ = _iterable_size
        elif 0 <= to_ < _iterable_size:
            pass
        elif (-_iterable_size) <= to_ < 0:
            to_ = _iterable_size + to_
        else:
            raise IndexError(f"index {from_} out of range")

        if step is not None:
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

        if (self._max_step is not None) and (self._current_step >= self._max_step):
            raise StopIteration

        current_loop, step_in_loop = divmod(self._current_step, self._size)

        if (self._max_loop is not None) and (current_loop >= self._max_loop):
            raise StopIteration

        if self._restart and (step_in_loop < self._step):
            step_in_loop = 0
            increment = (self._step - step_in_loop)
        else:
            increment = self._step

        self._current_step += increment

        pos = self._from + step_in_loop

        return self._iterable[pos]


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

    def range(self, from_=None, to_=None, step=1, max_loop=1, max_step=None, restart_loop=False):
        return IterView(self._list, from_=from_, to_=to_, step=step,
                        max_loop=max_loop, max_step=max_step, restart_loop=restart_loop)

