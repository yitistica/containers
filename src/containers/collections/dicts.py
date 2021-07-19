from collections.abc import ItemsView, KeysView, ValuesView

from containers.core.base import BaseMap
from containers.collections.sets import OrderedSet


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


class LocateView(object):
    def __init__(self, mapping):
        self._mapping = mapping

    def _get_item_from_tuple(self, item_tuple):
        cur = self._mapping
        for item in item_tuple:
            try:
                cur = cur[item]
            except KeyError:
                return False, None

        return True, cur

    def _delete_item_from_tuple(self, item_tuple):
        cur = self._mapping
        _parent = None
        for index, item in enumerate(item_tuple):
            if item not in cur:
                return False
            elif index == (len(item_tuple)-1):
                del cur[item]
            else:
                cur = cur[item]

        return True

    def __getitem__(self, item):
        if_exist, value = self._get_item_from_tuple((item,))  # check if the item exists first;

        if (not if_exist) and isinstance(item, tuple):
            if_exist, value = self._get_item_from_tuple(item)

        return if_exist, value

    def __delitem__(self, item):
        if_exist = self._delete_item_from_tuple((item,))  # check if the item exists first;

        if (not if_exist) and isinstance(item, tuple):
            if_exist = self._delete_item_from_tuple(item)

        return if_exist


class OrderedDict(BaseMap):
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


class LaissezDict(BaseMap):
    def __init__(self, iterable):
        super().__init__(iterable=iterable)

    @property
    def loc(self):
        return LocateView(mapping=self)

