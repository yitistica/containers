"""
pop by condition;
"""
from containers.core.base import MutableMappingBase
from containers.collections.elementary.sets import OrderedSet
from containers.collections.elementary.views.common import DictMapView, CallableMapView, StrView
from containers.collections.elementary.views.mapping import OrderedItemsView
from containers.collections.elementary.views.mapping import MappingView, LocateView, RecursiveLocateView


class Dict(MutableMappingBase):
    def __init__(self, iterable=()):
        super().__init__(iterable=iterable)


class OrderedDict(Dict):
    def __init__(self, iterable=()):
        self._ordered_keys = OrderedSet()
        super().__init__(iterable=iterable)

    def _get_item(self, key):
        return self._mapping[key]

    def _set_item(self, key, value):
        if key in self._ordered_keys:
            self._mapping[key] = value
        else:
            self._ordered_keys.add(key)
            self._mapping[key] = value

    def _delete_item(self, key):
        del self._mapping[key]
        self._ordered_keys.discard(key)

    def __iter__(self):
        return iter(self._ordered_keys)

    def items(self):
        return OrderedItemsView(mapping=self._mapping, ordered_keys=self._ordered_keys).ordered_items()

    def keys(self):
        return OrderedItemsView(mapping=self._mapping, ordered_keys=self._ordered_keys).ordered_keys()

    def values(self):
        return OrderedItemsView(mapping=self._mapping, ordered_keys=self._ordered_keys).ordered_values()


class XDict(Dict):
    def __init__(self, iterable=()):
        super().__init__(iterable=iterable)

    def mapping_view(self):
        return MappingView(mapping=self._mapping)

    @property
    def loc(self):
        return LocateView(mapping_view=self.mapping_view())

    @property
    def rloc(self):
        return RecursiveLocateView(mapping_view=self.mapping_view())

    def map(self, *args, **kwargs):
        return DictMapView(self.mapping_view(), *args, **kwargs)

    def apply(self, *args, params=None, **kwargs):
        return CallableMapView(self.mapping_view(), *args, params=params, **kwargs)

    @property
    def str(self):
        return StrView(iterable_view=self.mapping_view())

    def iter(self, *args, **kwargs):
        pass

    def order(self, key_order=None):
        pass


class OrderedXDict(OrderedDict, XDict):
    pass