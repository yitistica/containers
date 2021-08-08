"""

sequential: index, index is generated;

composition-wise setting;


view:
    retrieve view;


add mapping;

add_apply_mapping(mapping_name, mapping, default)
add_dict_mapping()



"""
from typing import Any

from containers.collections.elementary.views.base import Iterable
from containers.collections.elementary.common.iterators import MixedSliceIndexIter
from containers.collections.elementary.common.map_apply import CallableMapper, DictMapper, Mappers

from containers.core.common import isinstance_mapping
from containers.core.base import reinstantiate_iterable


class SequenceViewBase(Iterable):
    def __init__(self, sequence=()):
        super().__init__(iterable=sequence)

    @property
    def size(self):
        return len(self.iterable)


class IndexLocateView(object):
    def __init__(self, sequence):
        self._iterable = sequence

        self._size = len(self._iterable)

    def _get_by_index(self, index):
        if isinstance(index, int):
            sub_sequence = [self._iterable[index]]
        elif isinstance(index, slice):
            sub_sequence = self._iterable[index]
        else:
            raise TypeError(f"index {index} is not a valid index.")

        return reinstantiate_iterable(self, iterable=sub_sequence)

    def _get_by_indices(self, indices):
        sub_sequence = list()
        if isinstance(indices, (int, slice)):
            sub_sequence += self._get_by_index(index=indices)
        elif isinstance(indices, tuple):  # multiple;
            for index in indices:
                sub_sequence += self._get_by_index(index=index)
        else:
            raise TypeError(f"indices/index {indices} is not a valid index.")

        return reinstantiate_iterable(self, iterable=sub_sequence)

    def _set_by_index(self, index, value):
        """
        Make sure index to value is 1-to-1, e.g., confusion arises when a slice is mapped with a single value.
        :param index: int, or slice.
        :param value: Any or Iterable, in the case of slice, an iterable should be given.
        :return:
        """
        self._iterable[index] = value

    def _set_by_indices(self, indices, values):
        indices_inter = MixedSliceIndexIter(indices=indices, size=self._size)
        for which, index in enumerate(indices_inter):
            self._set_by_index(index, values[which])

    def __getitem__(self, indices):
        values = self._get_by_indices(indices=indices)
        return values

    def __setitem__(self, indices, values):
        self._set_by_indices(indices=indices, values=values)

    def _delete_by_index(self, index):
        del self._iterable[index]

    def __delitem__(self, indices):
        indices = list(set(MixedSliceIndexIter(indices=indices, size=self._size)))
        indices.sort(reverse=True)
        for index in indices:
            self._delete_by_index(index=index)


"""
IndexViewBase
"""


class IndexIterator(object):

    def __init__(self, iterable_size, from_=None, to_=None, step=1,
                 max_step=-1, max_cycle=None, max_leap=None, restart=False):

        assert (isinstance(iterable_size, int) and (iterable_size >=0))
        self._iterable_size = iterable_size

        if max_step == -1:
            max_step = iterable_size - 1
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

        _iterable_size = self._iterable_size

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

        return cycles, cycle_pos, ltr_pos, index

    def __iter__(self):
        return self

    def __next__(self):
        if (self._max_leap is not None) and (self._current_leap > self._max_leap):
            raise StopIteration

        if (self._max_step is not None) and (self._current_step > self._max_step):
            raise StopIteration

        cycles, cycle_pos, ltr_pos, index = self._convert_step_to_pos(self._current_step)

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

        return index


class IterIndexView(SequenceViewBase):
    def __init__(self, iterable=(), **kwargs):

        super().__init__(sequence=iterable)
        self._iterator = IndexIterator(self.size, **kwargs)

    def __iter__(self):
        return self

    def __next__(self):
        index = self._iterator.__next__()
        return index, self.iterable[index]



class IndexMapView(IterIndexView):
    def __init__(self, mapping, iterable, **kwargs):
        self._mapping = self._parse_mapping(mapping=mapping)

        super().__init__(iterable, **kwargs)

    @staticmethod
    def _parse_mapping(mapping):
        assert callable(mapping)
        return mapping



class IterIndexMapView(IterIndexView):
    def __init__(self, mapping, iterable, **kwargs):
        self._mapping = self._parse_mapping(mapping=mapping)

        super().__init__(iterable, **kwargs)

    @staticmethod
    def _parse_mapping(mapping):
        assert callable(mapping)
        return mapping

    def _map(self, value):
        return self._mapping(value)

    def __next__(self):
        index, value = super().__next__()
        return index, self._map(value=value)


class IterIndexDictMapView(IterIndexMapView):
    def __init__(self, mapping, mapping_default: Any = EmptyDefault, iterable=(),  **kwargs):
        self._mapping = self._parse_mapping(mapping=mapping)
        self._default = mapping_default

        super().__init__(iterable, **kwargs)

    @staticmethod
    def _parse_mapping(mapping):
        assert isinstance_mapping(mapping)
        return mapping

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


class BoolFilterView(IterIndexMapView):
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


a = IterIndexView([1,2,3])

for i in a:
    print(i)