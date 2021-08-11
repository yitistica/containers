"""
"""
import re

from containers.collections.elementary.views.base import Iterable
from containers.collections.elementary.common.iterators import MixedSliceIndexIter
from containers.collections.elementary.common.map_apply import CallableMapperCollector, \
    DictMapperCollector, EmptyDefault, Any
from containers.core.base import reinstantiate_iterable


class SequenceViewBase(Iterable):
    def __init__(self, sequence=()):
        super().__init__(iterable=sequence)

    @property
    def size(self):
        return len(self.iterable)


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


class IterMapView(IterIndexView):
    def __init__(self, map_view, **kwargs):
        super().__init__(iterable=map_view.iterable, **kwargs)
        self._map_view = map_view

    def __iter__(self):
        return self

    def __next__(self):
        index, value = IterIndexView.__next__(self)
        return index, value, self._map_view[index]


class MapViewBase(SequenceViewBase):
    def __init__(self, sequence, collector_cls):
        super().__init__(sequence=sequence)
        self._mappers = collector_cls()

    def add(self, mapper, name=None, *args, **kwargs):
        self._mappers.add(mapper=mapper, name=name, *args, **kwargs)

    def map(self, index, names=None):
        value = self.iterable[index]

        if names is None:
            pass
        elif not isinstance(names, (set, list)):
            return self._mappers.map(name=names, value=value)

        mapped = self._mappers.multi_map(names=names, value=value)

        return mapped

    @staticmethod
    def _parse_item(item):
        if isinstance(item, int):
            index, names = item, None
        elif isinstance(item, tuple):  # mappers;
            index, names = item
        else:
            raise TypeError(f"item {item} cannot be parsed, only int or tuple (sized 2) is accepted.")

        return index, names

    def __getitem__(self, item):
        index, names = self._parse_item(item=item)
        return self.map(index=index, names=names)

    def iter(self, **kwargs):
        return IterMapView(map_view=self, **kwargs)


class DictMapView(MapViewBase):
    def __init__(self, *args, sequence=(), default: Any = EmptyDefault, **kwargs):
        super().__init__(sequence=sequence, collector_cls=DictMapperCollector)

        if (len(args) == 1) and (len(kwargs) == 0):
            self.add(mapper=args[0], name=None, default=default)
        else:
            for name, mapper in enumerate(args):
                self.add(mapper=mapper, name=name, default=default)
            for name, mapper in kwargs.items():
                self.add(mapper=mapper, name=name, default=default)


class CallableMapView(MapViewBase):
    def __init__(self, *args, sequence=(), params=None, **kwargs):
        super().__init__(sequence=sequence, collector_cls=CallableMapperCollector)

        if not params:
            params = dict()

        if (len(args) == 1) and (len(kwargs) == 0):
            self.add(mapper=args[0], name=None, **params)
        else:
            for name, mapper in enumerate(args):
                self.add(mapper=mapper, name=name, **params)
            for name, mapper in kwargs.items():
                self.add(mapper=mapper, name=name, **params)


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


class RegexView(CallableMapView):
    def __init__(self, sequence, patterns, output='both', find_all=False, coerce=True):
        arg_callables, kwarg_callables = self._parse_patterns_into_callable(patterns=patterns)
        params = self._parse_params(output=output, find_all=find_all, coerce=coerce)
        super().__init__(*arg_callables, sequence=sequence, params=params, **kwarg_callables)

    @staticmethod
    def _wrap_find(pattern):

        def _callabe(string, output='both', find_all=False, coerce=True):

            if coerce:
                string = str(string)

            results = []
            iterator = re.finditer(pattern, string)
            for match in iterator:
                if output == 'both':
                    result = (match.span(), match.group())
                elif output == 'value':
                    result = match.group()
                elif output == 'span':
                    result = match.span()
                elif output == 'count':
                    result = 1
                else:
                    raise KeyError(f"output {output} can only take both, value or span.")

                if not find_all:
                    return result
                else:
                    results.append(result)

            if output == 'count':
                return len(results)
            else:
                return results

        return _callabe

    @staticmethod
    def _parse_patterns_into_callable(patterns):
        arg_callables, kwarg_callables = list(), dict()
        if isinstance(patterns, str):
            arg_callables = [RegexView._wrap_find(patterns)]
        elif isinstance(patterns, (list, tuple)):
            kwarg_callables = dict()
            for pattern in patterns:
                kwarg_callables[pattern] = RegexView._wrap_find(pattern)
        elif isinstance(patterns, dict):
            kwarg_callables = dict()
            for name, pattern in patterns.items():
                kwarg_callables[name] = RegexView._wrap_find(pattern)
        else:
            raise ValueError(f"patterns by type {type(patterns)} is not accepted.")

        return arg_callables, kwarg_callables

    @staticmethod
    def _parse_params(**kwargs):
        return kwargs


class RegexSubView(CallableMapView):
    def __init__(self, sequence, pattern, replacement, count=0, flags=0, coerce=True):
        pattern_callabe = self._parse_pattern_into_callable(pattern=pattern)
        params = self._parse_params(replacement=replacement, count=count, flags=flags, coerce=coerce)
        super().__init__(pattern_callabe, sequence=sequence, params=params)

    @staticmethod
    def _wrap_sub(pattern):

        def _callabe(string, replacement, count=0, flags=0, coerce=True):

            if coerce:
                string = str(string)

            string = re.sub(pattern=pattern, repl=replacement, string=string, count=count, flags=flags)

            return string

        return _callabe

    @staticmethod
    def _parse_pattern_into_callable(pattern):
        if isinstance(pattern, str):
            callable_ = RegexSubView._wrap_sub(pattern)
        else:
            raise ValueError(f"pattern by type {type(pattern)} is not accepted.")

        return callable_

    @staticmethod
    def _parse_params(**kwargs):
        return kwargs


class StrView(SequenceViewBase):
    """
    start view,
    subsitute,
    """
    def __init__(self, sequence):
        super().__init__(sequence=sequence)

    def regex(self, patterns, output='both', find_all=False, coerce=True):
        return RegexView(sequence=self.iterable, patterns=patterns, output=output, find_all=find_all, coerce=coerce)

    def contain(self, patterns):
        regex_view = RegexView(sequence=self.iterable, patterns=patterns, output='count', find_all=False, coerce=True)
        return regex_view

    def sub(self, pattern, replacement, count=0, flags=0, coerce=True):
        sub_view = RegexSubView(sequence=self.iterable, pattern=pattern, replacement=replacement,
                                count=count, flags=flags, coerce=coerce)
        return sub_view


class FilterView(object):
    pass



class BoolView(CallableMapView):
    pass


class BoolFilterView(IterMapView):
    """only for """
    pass



class GroupByView(object):
    pass


class Rolling(object):
    def __init__(self):
        pass


