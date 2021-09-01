from containers.core.base import MutableSequenceBase
from containers.collections.elementary.views.common import DictMapView, \
    CallableMapView, StrView
from containers.collections.elementary.views.sequential import SequenceView, \
    LocateView


class InvalidCategoryValueError(Exception):
    def __init__(self, value, category):
        message = f'Given value {value} is not of part of <{category}> .'
        super().__init__(message)


class CommonSequentialExtension(MutableSequenceBase):

    def __init__(self, sequence):
        super().__init__(iterable=sequence)

    def sequence_view(self):
        return SequenceView(sequence=self._list)

    def iter(self, *args, **kwargs):
        return self.sequence_view().iter(*args, **kwargs)

    def map(self, *args, **kwargs):
        view = DictMapView(*args, **kwargs)
        view.set_iterable_view(iterable_view=self.sequence_view())
        return view

    def apply(self, *args, params=None, **kwargs):
        view = CallableMapView(*args, params=params, **kwargs)
        view.set_iterable_view(iterable_view=self.sequence_view())
        return view

    @property
    def iloc(self):
        return LocateView(sequence_view=self.sequence_view())


class XList(CommonSequentialExtension):

    @property
    def str(self):
        return StrView(iterable_view=self.sequence_view())
