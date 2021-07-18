from collections.abc import MutableMapping, Sequence, MutableSequence, MutableSet, Set


class BaseMixin:
    def __repr__(self):
        return f"{self.__class__.__name__}({self.__str__()})"


class FrozenSequence(Sequence, BaseMixin):
    def __init__(self, iterable=()):
        self._tuple = tuple(iterable)

    def __getitem__(self, index):
        return self._tuple[index]

    def __len__(self):
        return len(self._tuple)

    def __str__(self):
        return str(self._tuple)


class BaseSequence(MutableSequence, BaseMixin):
    def __init__(self, iterable=()):
        self._list = list()
        self.extend(iterable)  # a loop that uses append, which uses insert method;

    def _get_item(self, index):
        return self._list[index]

    def __getitem__(self, index):
        return self._get_item(index=index)

    def _set_item(self, index, value):
        """
        here if key is greater than the max of index,
        """
        self._list[index] = value

    def __setitem__(self, index, value):
        self._set_item(index=index, value=value)

    def _delete_item(self, index):
        del self._list[index]

    def __delitem__(self, index):
        self._delete_item(index)

    def __len__(self):
        return len(self._list)

    def insert(self, index, value):
        self._list.insert(index, value)

    def __str__(self):
        return str(self._list)


class SetMixin:
    def union(self, iterable=()):
        return self | iterable

    def intersection(self, iterable=()):
        return self & iterable

    def difference(self, iterable=()):
        return self - iterable


class BaseFrozenSet(Set, SetMixin, BaseMixin):
    def __init__(self, iterable=()):
        self._set = frozenset(iterable)

    def __contains__(self, element):
        return element in self._set

    def __iter__(self):
        return iter(self._set)

    def __len__(self):
        return len(self._set)

    def __str__(self):
        return str(self._set)


class BaseSet(MutableSet, SetMixin, BaseMixin):
    def __init__(self, iterable=()):
        self._set = set()
        self.update(iterable)

    def _add(self, element):
        self._set.add(element)

    def add(self, element):
        self._add(element)

    def update(self, iterable):
        for element in iterable:
            self.add(element)

    def _discard(self, element):
        self._set.discard(element)

    def discard(self, element):
        self._discard(element)

    def __len__(self):
        return len(self._set)

    def __iter__(self):
        return iter(self._set)

    def __contains__(self, element):
        return element in self._set

    def __str__(self):
        return str(self._set)


class BaseMap(MutableMapping, BaseMixin):
    def __init__(self, iterable=()):
        self._mapping = dict()
        self.update(iterable)

    def _get_item(self, key):
        return self._mapping[key]

    def __getitem__(self, key):
        return self._get_item(key=key)

    def _set_item(self, key, value):
        self._mapping[key] = value

    def __setitem__(self, key, value):
        self._set_item(key=key, value=value)

    def _delete_item(self, key):
        del self._mapping[key]

    def __delitem__(self, key):
        self._delete_item(key=key)

    def __iter__(self):
        return iter(self._mapping)

    def __len__(self):
        return len(self._mapping)

    def __contains__(self, key):
        return key in self._mapping

    def __str__(self):
        return str(self._mapping)
