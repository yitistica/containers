
from containers.collections.elementary.views.base import LocationIterator, IterableView


class MappingLocationIterator(LocationIterator):

    def __init__(self, mapping):
        locator_iterator = iter(mapping.keys())
        super().__init__(locator_iterator=locator_iterator)


class MappingView(IterableView):
    def __init__(self, mapping):
        super().__init__(iterable=mapping)

    @property
    def size(self):
        return len(self.iterable)

    def iter_loc(self, *args, **kwargs):
        return MappingLocationIterator(mapping=self.iterable)


class LocateView(object):
    def __init__(self, mapping_view):
        self.mapping_view = mapping_view

    @property
    def mapping(self):
        return self.mapping_view.iterable

    def _get_by_key(self, key):
        sub_mapping = [(key, self.mapping[key]), ]
        return sub_mapping

    def _get_by_keys(self, keys):
        sub_mapping = list()
        try:
            sub_mapping += self._get_by_key(key=keys)  # try retrieving in case tuple obj was used as a key.
        except KeyError as e:
            if isinstance(keys, tuple):  # multiple;
                for index in keys:
                    sub_mapping += self._get_by_key(key=index)
            else:
                raise e
        return self.mapping_view.reinstantiate(iterable=sub_mapping)

    def _set_by_key(self, key, value):
        self.mapping[key] = value

    def _set_by_keys(self, keys, values):
        for which, key in enumerate(keys):
            self._set_by_key(key, values[which])

    def __getitem__(self, keys):
        values = self._get_by_keys(keys=keys)
        return values

    def __setitem__(self, indices, values):
        self._set_by_keys(keys=indices, values=values)

    def _delete_by_key(self, key):
        del self.mapping[key]

    def __delitem__(self, keys):
        for key in keys:
            self._delete_by_key(key=key)


class RecursiveLocateView(object):
    def __init__(self, mapping_view):
        self.mapping_view = mapping_view

    @property
    def mapping(self):
        return self.mapping_view.iterable

    def _get_item_from_tuple(self, item_tuple):
        cur = self.mapping
        for item in item_tuple:
            try:
                cur = cur[item]
            except KeyError:
                return False, None

        return True, cur

    def _set_item_from_tuple(self, item_tuple, value):
        cur = self.mapping
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
        cur = self.mapping
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
        if_exist, value = self._get_if_exists(item=item)

        if not if_exist:
            raise KeyError(f"keys {item} does not exist.")

        return value

    def __setitem__(self, item, value):
        if_exist = self._set_if_exists(item=item, value=value)

        if not if_exist:
            raise KeyError(f"keys {item} does not exist.")

    def __delitem__(self, item):
        if_exist = self._delete_if_exists(item)

        if not if_exist:
            raise KeyError(f"keys {item} does not exist.")