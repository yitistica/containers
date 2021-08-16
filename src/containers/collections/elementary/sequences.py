from containers.core.base import MutableSequenceBase
from containers.collections.elementary.views.common import DictMapView, CallableMapView, StrView
from containers.collections.elementary.views.sequential import SequenceView, LocateView
from containers.collections.elementary.sets import OrderedSet
from containers.core.common import remove_repeat


class InvalidCategoryValueError(Exception):
    def __init__(self, value, category):
        message = f'Given value {value} is not of part of <{category}> .'
        super().__init__(message)


class XList(MutableSequenceBase):

    def __init__(self, sequence):
        super().__init__(iterable=sequence)

    def sequence_view(self):
        return SequenceView(sequence=self._list)

    def iter(self, *args, **kwargs):
        return self.sequence_view().iter(*args, **kwargs)

    def map(self, *args, **kwargs):
        return DictMapView(self.sequence_view(), *args, **kwargs)

    def apply(self, *args, params=None, **kwargs):
        return CallableMapView(self.sequence_view(), *args, params=params, **kwargs)

    @property
    def iloc(self):
        return LocateView(sequence_view=self.sequence_view())

    @property
    def str(self):
        return StrView(iterable_view=self.sequence_view())


class XSetSequence(OrderedSet, XList):
    def __init__(self, iterable=()):
        iterable = remove_repeat(iterable, keep_first=False)
        XList.__init__(self, sequence=iterable)
