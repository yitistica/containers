from containers.collections.elementary.views.sequential import IndexIterator
from containers.collections.elementary.views.sequential import DictMapView, CallableMapView
from containers.collections.elementary.views.sequential import StrView
from containers.collections.elementary.views.sequential import IndexLocateView
from containers.core.base import MutableSequenceBase


class InvalidCategoryValueError(Exception):
    def __init__(self, value, category):
        message = f'Given value {value} is not of part of <{category}> .'
        super().__init__(message)


class CategorySequence(MutableSequenceBase):
    def __init__(self, categories):

        super().__init__()

    def _set_item(self, index, value):

        self._list[index] = value


class StatisticsView(object):
    pass

    def apply(self):
        pass

    def count(self):
        pass


class RandomView(object):
    pass


class XList(MutableSequenceBase):

    def iter(self, from_=None, to_=None, step=1, max_step=-1, max_cycle=None, max_leap=None, restart=False):
        return IndexIterator(self._list, from_=from_, to_=to_, step=step,
                             max_step=max_step, max_cycle=max_cycle, max_leap=max_leap, restart=restart)

    def map(self, *args, **kwargs):
        return DictMapView(*args, sequence=self._list, **kwargs)

    def apply(self, *args, params=None, **kwargs):
        return CallableMapView(*args, sequence=self._list, params=params, **kwargs)

    @property
    def iloc(self):
        return IndexLocateView(sequence=self._list)

    @property
    def str(self):
        return StrView()

