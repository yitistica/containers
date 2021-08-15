
from containers.collections.elementary.views.base import LocationIterator, IterableView
from containers.collections.elementary.common.iterators import MixedSliceIndexIter, IndexIterator
from containers.collections.elementary.views.common import CallableMapView, MapIterView


class SequenceLocationIterator(LocationIterator):

    def __init__(self, sequence, from_=None, to_=None, step=1,
                 max_step=-1, max_cycle=None, max_leap=None, restart=False):
        size = len(sequence)
        locator_iterator = IndexIterator(iterable_size=size, from_=from_, to_=to_, step=step,
                                         max_step=max_step, max_cycle=max_cycle, max_leap=max_leap, restart=restart)
        super().__init__(locator_iterator=locator_iterator)


class SequenceView(IterableView):
    def __init__(self, sequence):
        super().__init__(iterable=sequence)

    @property
    def size(self):
        return len(self.iterable)

    def iter_loc(self, *args, **kwargs):
        return SequenceLocationIterator(sequence=self.iterable, *args, **kwargs)


class LocateView(object):
    def __init__(self, sequence_view):
        self.sequence_view = sequence_view

    def _get_by_index(self, index):
        if isinstance(index, int):
            sub_sequence = [self.sequence_view[index]]
        elif isinstance(index, slice):
            sub_sequence = self.sequence_view[index]
        else:
            raise TypeError(f"index {index} is not a valid index.")

        return sub_sequence

    def _get_by_indices(self, indices):
        sub_sequence = list()
        if isinstance(indices, (int, slice)):
            sub_sequence += self._get_by_index(index=indices)
        elif isinstance(indices, tuple):  # multiple;
            for index in indices:
                sub_sequence += self._get_by_index(index=index)
        else:
            raise TypeError(f"indices/index {indices} is not a valid index.")

        return self.sequence_view.reinstantiate(iterable=sub_sequence)

    def _set_by_index(self, index, value):
        """
        Make sure index to value is 1-to-1, e.g., confusion arises when a slice is mapped with a single value.
        :param index: int, or slice.
        :param value: Any or Iterable, in the case of slice, an iterable should be given.
        :return:
        """
        self.sequence_view[index] = value

    def _set_by_indices(self, indices, values):
        indices_inter = MixedSliceIndexIter(indices=indices, size=self.sequence_view.size)
        for which, index in enumerate(indices_inter):
            self._set_by_index(index, values[which])

    def __getitem__(self, indices):
        values = self._get_by_indices(indices=indices)
        return values

    def __setitem__(self, indices, values):
        self._set_by_indices(indices=indices, values=values)

    def _delete_by_index(self, index):
        del self.sequence_view[index]

    def __delitem__(self, indices):
        indices = list(set(MixedSliceIndexIter(indices=indices, size=self.sequence_view.size)))
        indices.sort(reverse=True)
        for index in indices:
            self._delete_by_index(index=index)


class BoolView(CallableMapView):
    pass


class CompareView(MapIterView):
    """rely on bool view;
     compare with another iterable;

     """
    pass


class BoolFilterView(MapIterView):
    """only for """
    pass


class FilterView(object):
    pass


class GroupByView(object):
    pass


class RollingIndexIter(object):
    def __iter__(self, size, kernel_size, stride, left_padding, right_padding):
        self._index_iterator = IndexIterator(size,
                                             from_=None, to_=None, step=stride,
                                             max_step=-1, max_cycle=None, max_leap=None, restart=False)

    @staticmethod
    def _parse_params(size, kernel_size, stride):
        # off short
        pass


class RollingIterView(SequenceView):
    """
    after each, store
    """

    def __init__(self, iterable=(), **kwargs):
        super().__init__(sequence=iterable)
        self._index_iterator = IndexIterator(self.size, **kwargs)

    def __iter__(self):
        return self

    def __next__(self):
        index = self._index_iterator.__next__()
        return index, self.iterable[index]
