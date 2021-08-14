from collections.abc import ItemsView, KeysView, ValuesView

from containers.core.base import MutableMappingBase
from containers.collections.elementary.views.mapping import MappingView, LocateView, RecursiveLocateView
from containers.collections.elementary.views.common import DictMapView, CallableMapView, StrView
from containers.collections.elementary.sets import OrderedSet


class Dict(MutableMappingBase):
    def __init__(self, iterable):
        super().__init__(iterable=iterable)


class XDict(Dict):
    def __init__(self, iterable):
        super().__init__(iterable=iterable)
        self.mapping_view = MappingView(mapping=self._mapping)

    @property
    def loc(self):
        return LocateView(mapping_view=self.mapping_view)

    @property
    def rloc(self):
        return RecursiveLocateView(mapping_view=self.mapping_view)

    def map(self, *args, **kwargs):
        return DictMapView(self.mapping_view, *args, **kwargs)

    def apply(self, *args, params=None, **kwargs):
        return CallableMapView(self.mapping_view, *args, params=params, **kwargs)

    @property
    def str(self):
        return StrView(iterable_view=self.mapping_view)


class _CommonOrderedMapView:

    @classmethod
    def _from_iterable(cls, it):
        return OrderedSet(it)


class OrderedItemsView(ItemsView, _CommonOrderedMapView):

    def __iter__(self):
        for key in self._mapping._ordered_key:
            yield (key, self._mapping[key])


class OrderedKeysView(KeysView, _CommonOrderedMapView):

    def __iter__(self):
        yield from self._mapping._ordered_key


class OrderedValuesView(ValuesView, _CommonOrderedMapView):

    def __iter__(self):
        for key in self._mapping._ordered_key:
            yield self._mapping[key]


class OrderedDict(Dict):
    def __init__(self, iterable=()):
        self._ordered_key = OrderedSet()
        super().__init__(iterable=iterable)

    def _get_item(self, key):
        return self._mapping[key]

    def _set_item(self, key, value):
        if key in self._ordered_key:
            self._mapping[key] = value
        else:
            self._ordered_key.add(key)
            self._mapping[key] = value

    def _delete_item(self, key):
        del self._mapping[key]
        self._ordered_key.discard(key)

    def __iter__(self):
        return iter(self._ordered_key)

    def items(self):
        return OrderedItemsView(self)

    def keys(self):
        return OrderedKeysView(self)

    def values(self):
        return OrderedValuesView(self)
