"""
given one iterable:
    build two iterator:
        locator:
        value:

any iterator based view: should be able to be shared between mapping and sequence;

only need an iterator to loop over

locator based view:

multiple indices

view has get method, multiple gets, and inter

"""


class ViewBase(object):
    def __init__(self, *args, **kwargs):
        pass


class LocationIterator(object):
    def __init__(self, locator_iterator):
        self._iterator = locator_iterator  # keys()

    def __iter__(self):
        return self

    def __next__(self):
        item = self._iterator.__next__()
        return item


class MappingLocationIterator(LocationIterator):

    def __init__(self, mapping):
        locator_iterator = iter(mapping.keys())
        super().__init__(locator_iterator=locator_iterator)


class SequenceLocationIterator(LocationIterator):

    def __init__(self, sequence):
        size = len(sequence)
        locator_iterator = IndexIterator(iterable_size=size, from_=None, to_=None, step=1,
                                         max_step=-1, max_cycle=None, max_leap=None, restart=False)
        super().__init__(locator_iterator=locator_iterator)

    def __iter__(self):
        return self


class IterableWrapView(ViewBase):
    """
    base view for an iterable
    """
    def __init__(self, iterable):
        self._iterable = iterable
        super().__init__()

    @property
    def iterable(self):
        return self._iterable

    def locator(self):
        return NotImplemented

    def value(self):
        return NotImplemented

    @property
    def size(self):
        return NotImplemented


class IterLocatorView(IterableWrapView):
    def __init__(self, iterable=(), **kwargs):
        super().__init__(iterable=iterable)
        self._iterator = IndexIterator(self.size, **kwargs)

    def __iter__(self):
        return self

    def __next__(self):
        index = self._iterator.__next__()
        return index, self.iterable[index]


class IterMappingView(object):

    def __init__(self, mapping):
        self._mapping = mapping
        self.key = iter(mapping.keys())
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        key = self.key.__next__()


class SequenceViewBase(IterableWrapView):
    def __init__(self, sequence=()):
        super().__init__(iterable=sequence)

    @property
    def size(self):
        return len(self.iterable)


a  = {1:2, 2:3, 3:4}
b = LocationIterator(a.keys())

for i in b:
    print(i)


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
        self._index_iterator = IndexIterator(self.size, **kwargs)

    def __iter__(self):
        return self

    def __next__(self):
        index = self._index_iterator.__next__()
        return index, self.iterable[index]