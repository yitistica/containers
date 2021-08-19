from containers.collections.elementary.common.iterators import IndexIterator
from containers.collections.elementary.views.sequential import SequenceView


class StatisticsView(object):
    pass

    def apply(self):
        pass

    def count(self):
        pass


class RandomView(object):
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


class RollingIndexIter(object):
    def __iter__(self, size, kernel_size, stride, left_padding, right_padding):
        self._index_iterator = IndexIterator(size,
                                             from_=None, to_=None, step=stride,
                                             max_step=-1, max_cycle=None, max_leap=None, restart=False)

    @staticmethod
    def _parse_params(size, kernel_size, stride):
        # off short
        pass
