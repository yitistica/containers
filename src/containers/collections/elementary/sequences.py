from containers.core.base import BaseSequence, BaseSet, BaseFrozenSet
from containers.collections.elementary.common import ElementView, IterView, IndexLocateView, DictMapView, ApplyView


class InvalidCategoryValueError(Exception):
    def __init__(self, value, category):
        message = f'Given value {value} is not of part of <{category}> .'
        super().__init__(message)


class CategorySequence(BaseSequence):
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


class XList(BaseSequence):

    def iter(self, from_=None, to_=None, step=1, max_step=-1, max_cycle=None, max_leap=None, restart=False):
        return IterView(self._list, from_=from_, to_=to_, step=step,
                        max_step=max_step, max_cycle=max_cycle, max_leap=max_leap, restart=restart)

    def map(self, mapping, **kwargs):
        if isinstance(mapping, dict):
            return DictMapView(iterable=self._list, mapping=mapping, **kwargs)
        elif callable(mapping):
            return ApplyView(iterable=self._list, mapping=mapping)
        else:
            TypeError(f"mapping {type(mapping)} is not supported.")

    @property
    def iloc(self):
        return IndexLocateView(iterable=self._list)
