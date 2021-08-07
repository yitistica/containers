from collections.abc import ItemsView, KeysView, ValuesView

from containers.core.base import MutableMappingBase
from containers.collections.elementary.sets import OrderedSet


class Dict(MutableMappingBase):
    def __init__(self, iterable):
        super().__init__(iterable=iterable)


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


class GetLocateView(object):
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

    def _set_item_from_tuple(self, item_tuple, value):
        cur = self._mapping
        _parent = None
        for index, item in enumerate(item_tuple):
            if item not in cur:
                return
            elif index == (len(item_tuple)-1):
                cur[item] = value
            else:
                cur = cur[item]

        return True

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

    def _get_if_exists(self, item):
        if_exist, value = self._get_item_from_tuple((item,))  # check if the item exists first;

        if (not if_exist) and isinstance(item, tuple):
            if_exist, value = self._get_item_from_tuple(item)

        return if_exist, value

    def _set_if_exists(self, item, value):
        if_exist = self._set_item_from_tuple((item,), value)

        if (not if_exist) and isinstance(item, tuple):
            if_exist = self._set_item_from_tuple(item, value)

        return if_exist

    def _delete_if_exists(self, item):
        if_exist = self._delete_item_from_tuple((item,))

        if (not if_exist) and isinstance(item, tuple):
            if_exist = self._delete_item_from_tuple(item)

        return if_exist

    def __getitem__(self, item):
        return self._get_if_exists(item=item)

    def __setitem__(self, item, value):
        self._set_if_exists(item=item, value=value)

    def __delitem__(self, item):
        self._delete_if_exists(item=item)


class LocateView(GetLocateView):
    def __getitem__(self, item):
        if_exist, value = self._get_if_exists(item=item)

        if not if_exist:
            raise KeyError(f"keys {item} does not exist.")

        return value

    def __setitem__(self, item, value):
        if_exist, value = self._set_if_exists(item=item, value=value)

        if not if_exist:
            raise KeyError(f"keys {item} does not exist.")

    def __delitem__(self, item):
        if_exist = self._delete_if_exists(item)

        if not if_exist:
            raise KeyError(f"keys {item} does not exist.")


class LaissezDict(Dict):
    def __init__(self, iterable):
        super().__init__(iterable=iterable)

    @property
    def loc(self):
        return LocateView(mapping=self)

    @property
    def get_loc(self):
        return GetLocateView(mapping=self)