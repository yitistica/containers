"""
implementation of set, sequence & mapping by collections.abc.
"""
from collections.abc import Mapping, MutableMapping, Sequence, MutableSequence, Set, MutableSet


def reinstantiate_iterable(obj, iterable):
    return obj.__class__(iterable)


class BaseMixin:

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__str__()})"


class SequenceBaseMinxin(BaseMixin):
    pass


class MappingBaseMinxin(BaseMixin):
    pass


class SetBaseMinxin(BaseMixin):
    pass


class SequenceBase(Sequence, SequenceBaseMinxin):
    def __init__(self, iterable=()):
        self._tuple = tuple(iterable)

    def __getitem__(self, index):
        return self._tuple[index]

    def __len__(self):
        return len(self._tuple)

    def __str__(self):
        return str(self._tuple)


class MutableSequenceBase(MutableSequence, SequenceBaseMinxin):
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


class SetMixin(SetBaseMinxin):
    def union(self, iterable=()):
        return self | iterable

    def intersection(self, iterable=()):
        return self & iterable

    def difference(self, iterable=()):
        return self - iterable


class SetBase(Set, SetMixin):
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


class MutableSetBase(MutableSet, SetMixin):
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


class MappingBase(Mapping, MappingBaseMinxin):
    def __init__(self, iterable=()):
        self._mapping = dict(iterable)

    def _get_item(self, key):
        return self._mapping[key]

    def __getitem__(self, key):
        return self._get_item(key=key)

    def __iter__(self):
        return iter(self._mapping)

    def __len__(self):
        return len(self._mapping)

    def __contains__(self, key):
        return key in self._mapping

    def __str__(self):
        return str(self._mapping)


class MutableMappingBase(MutableMapping, MappingBaseMinxin):
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
