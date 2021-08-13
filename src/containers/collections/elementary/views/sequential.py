"""
difference between sequence and mapping: key
index: value
key: value

chainable;


"""

from containers.collections.elementary.views.base import SequenceViewBase, IndexIterator
from containers.collections.elementary.common.iterators import MixedSliceIndexIter
from containers.collections.elementary.views.common import CallableMapView, IterMapView
from containers.core.base import reinstantiate_iterable


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


class BoolView(CallableMapView):
    pass


class CompareView(IterMapView):
    """rely on bool view;
     compare with another iterable;

     """
    pass


class BoolFilterView(IterMapView):
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





class RollingIterView(SequenceViewBase):
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