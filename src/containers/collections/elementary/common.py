"""
with dict.efilter(filter=True) as  filter, k, v:
    condtion_1 = lambda x: x > 2
    a = filter(conditon, select=)

slice(
"""
from typing import Any
from collections.abc import Iterable


class MixedSlices(object):
    def __init__(self, mix_slices=()):
        self._mix_slices = mix_slices

    def __iter__(self):
        return self

    def __next__(self):
        pass


class IndexLocateView(object):
    def __init__(self, iterable):
        self._iterable = iterable

        self._size = len(self._iterable)

    def _construct_iterable(self, iterable):
        return type(self._iterable)(iterable)

    def _get_by_index(self, index):
        if isinstance(index, int):
            subsequence = [self._iterable[index]]
        elif isinstance(index, slice):
            subsequence = self._iterable[index]
        else:
            raise TypeError(f"index {index} is not a valid index.")

        return self._construct_iterable(iterable=subsequence)

    def _get_by_indices(self, indices):
        subsequence = self._construct_iterable(iterable=())
        if isinstance(indices, (int, slice)):
            subsequence += self._get_by_index(index=indices)
        elif isinstance(indices, tuple):  # multiple;
            for index in indices:
                subsequence += self._get_by_index(index=index)
        else:
            raise TypeError(f"indices/index {indices} is not a valid index.")

        return subsequence

    def _set_by_index(self, index, values):
        """
        Make sure index to value is 1-to-1, e.g., confusion arises when a slice is mapped with a single value.
        :param index: int, or slice.
        :param value: Any or Iterable, in the case of slice, an iterable should be given.
        :return:
        """
        if isinstance(index, slice):
            for _index in range(*index.indices(len(self._iterable))):
                pass
        self._iterable[index] = values

    def _set_by_indices(self, indices, values):

        if isinstance(indices, (int, slice)):
            self._iterable[indices] = values
        elif isinstance(indices, tuple):  # multiple;
            for index in indices:
                self._iterable[index] = values
        else:
            raise TypeError(f"indices/index {indices} is not a valid index.")

    def __getitem__(self, indices):
        values = self._get_by_indices(indices=indices)
        return values

    def __setitem__(self, indices, values):
        self._set_by_indices(indices=indices, values=values)

    def __delitem__(self, item):
        pass


class IterView(object):

    def __init__(self, iterable, from_=None, to_=None, step=1,
                 max_step=-1, max_cycle=None, max_leap=None, restart=False):
        self._iterable = iterable

        if max_step == -1:
            max_step = len(self._iterable) - 1
        elif max_step:
            assert (isinstance(max_step, int) and max_step >= 0)
        self._max_step = max_step

        if max_cycle:
            assert (isinstance(max_cycle, int) and max_cycle >= 0)
        self._max_cycle = max_cycle

        if max_leap:
            assert (isinstance(max_leap, int) and max_leap >= 0)
        self._max_leap = max_leap

        assert isinstance(restart, bool)
        self._restart = restart

        # setting:
        self._from, self._to, self._step, self._direction = self._parse_range_args(from_=from_, to_=to_, step=step)
        self._size = self._to - self._from

        # state to track:
        self._current_leap = 0
        self._current_step = 0  # absolute value of steps;

    def _parse_range_args(self, from_, to_, step):

        _iterable_size = len(self._iterable)

        # range:
        if from_ is None:
            from_ = 0
        elif 0 <= from_ < _iterable_size:
            pass
        elif (-_iterable_size) <= from_ < 0:
            from_ = _iterable_size + from_
        else:
            raise IndexError(f"index {from_} out of range")
        assert isinstance(from_, int)

        if to_ is None:
            to_ = _iterable_size
        elif 0 <= to_ < _iterable_size:
            pass
        elif (-_iterable_size) <= to_ < 0:
            to_ = _iterable_size + to_
        else:
            raise IndexError(f"index {from_} out of range")
        assert isinstance(to_, int)

        if from_ > to_:
            raise ValueError(f"from_ position is greater than to_ position, "
                             f"use step < 0 to set reverse order.")

        # step:
        direction = 1
        if step is None:
            step = 1
        elif step < 0:
            direction = -1
        else:
            pass
        step = abs(step)  # only keep track of the magnitude;
        assert isinstance(step, int)

        return from_, to_, step, direction

    def _convert_step_to_pos(self, steps):
        """
        mapping from the number of taken steps to the index in the iterable.
        # step taken from right to left:
            if direction == -1: iterable is looped from right to left, the number of steps needed to complete a cycle
            is unchanged, but pos & index conversion is given as:
                             ['a', 'b', 'c', 'd']
            [l-to-r] index:    0,   1,   2,   3  = step
            [r-to-l] index:    3,   2,   1,   0  = size - step
        :param steps: int, the number of steps taken from start.
        :return:
            cycles: int, the number of times that subsequence of the iterable has been cycled through.
            cycle_pos: int, the position away from the first item (i.e., step=0) of the subsequence.
            ltr_pos: int, the position away from the left-most item of the subsequence.
            index: int, the index of the item that cycle_pos refers to.
            value: Any, the value of the item by the index.
        """
        cycles, cycle_pos = divmod(steps, self._size)  # divmod: Integer = quotient * divisor + remainder

        if self._direction == -1:
            ltr_pos = self._size - cycle_pos - 1  # to convert r-to-l index back to l-to-r index.
        else:
            ltr_pos = cycle_pos

        index = self._from + ltr_pos
        value = self._iterable[index]
        return cycles, cycle_pos, ltr_pos, index, value

    def __iter__(self):
        return self

    def __next__(self):

        if (self._max_leap is not None) and (self._current_leap > self._max_leap):
            raise StopIteration

        if (self._max_step is not None) and (self._current_step > self._max_step):
            raise StopIteration

        cycles, cycle_pos, ltr_pos, index, value = self._convert_step_to_pos(self._current_step)

        if (self._max_cycle is not None) and (cycles > self._max_cycle):
            raise StopIteration

        # setting current_step for the next candidate step:
        if self._restart:
            # can only leap as many as the remaining steps left in the cycle:
            next_step = min(self._step, self._size - cycle_pos)  # to go back to the 1st pos in the cycle.
        else:
            next_step = self._step

        self._current_leap += 1
        self._current_step += next_step

        return index, value


class IterViewByComposition(object):
    def __init__(self, iterable):
        self._iterator = IterView(iterable, from_=None, to_=None, step=1,
                                  max_step=-1, max_cycle=None, max_leap=None, restart=False)

    def __iter__(self):
        return self

    def __next__(self):
        return self._iterator.__next__()


class EmptyDefault(object):
    pass


class DictMapView(IterViewByComposition):
    def __init__(self, iterable, mapping, default: Any = EmptyDefault):
        super().__init__(iterable)
        assert isinstance(mapping, dict)
        self._mapping = mapping

        self._default = default

    def _map(self, value):
        try:
            return self._mapping[value]
        except KeyError as e:
            if self._default == EmptyDefault:
                raise e
            else:
                return self._default

    def __next__(self):
        index, value = super().__next__()
        return index, self._map(value=value)


class ApplyView(IterViewByComposition):
    def __init__(self, iterable, mapping):
        super().__init__(iterable)
        assert callable(mapping)
        self._mapping = mapping

    def _map(self, value):
        return self._mapping(value)

    def __next__(self):
        index, value = super().__next__()
        return index, self._map(value=value)


class BoolFilterView(ApplyView):
    """only for """
    pass


class FilterView(object):
    pass


class RegexFilter(object):
    pass


class GroupByView(object):
    pass


class ElementView(object):
    def __init__(self, type_, iterable):
        self._type = type_
        self._iterable = iterable


class EFilterView(object):
    pass


class Rolling(object):
    def __init__(self):
        pass


a = IndexLocateView([1,2, 3, 4,5])

for index, value in enumerate(range(2,10)):
    print(index, value)