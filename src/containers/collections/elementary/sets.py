from containers.core.base import SequenceBase, MutableSequenceBase, MutableSetBase
from containers.core.common import remove_repeat


class OrderedSetMixins:
    _list: list
    append = None
    _delete_item = None

    def which(self, value):
        index = None
        for i, _ in enumerate(self):
            if _ == value:
                index = i
                break

        return index

    def _set_item(self, index, value):
        self.insert(index=index, value=value)

    def insert(self, index, value):
        self._discard(value=value)
        self._list.insert(index, value)

    def _add(self, element):
        self.append(element)

    def _discard(self, value):
        index = self.which(value=value)
        if index is not None:
            self._delete_item(index=index)


class OrderedSet(OrderedSetMixins, MutableSetBase, MutableSequenceBase):
    def __init__(self, iterable=()):
        iterable = remove_repeat(iterable, keep_first=False)
        MutableSequenceBase.__init__(self, iterable=iterable)


class OrderedFrozenSet(OrderedSetMixins, SequenceBase):
    def __init__(self, iterable=()):
        iterable = remove_repeat(iterable)
        super().__init__(iterable=iterable)
