from collections.abc import ItemsView, KeysView, ValuesView

from containers.core.base import BaseMap
from containers.collections.sets import OrderedSet


class _CommonView:
    @classmethod
    def _from_iterable(cls, it):
        return OrderedSet(it)


class OrderedItemsView(ItemsView, _CommonView):

    def __iter__(self):
        for key in self._mapping._ordered_key:
            yield (key, self._mapping[key])


class OrderedKeysView(KeysView, _CommonView):

    def __iter__(self):
        yield from self._mapping._ordered_key


class OrderedValuesView(ValuesView, _CommonView):

    def __iter__(self):
        for key in self._mapping._ordered_key:
            yield self._mapping[key]


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

    def _get_exist_item(self, key):
        if key not in self._mapping:
            exist = False
        else:
            exist = True

        return exist, self._mapping.get(key)
