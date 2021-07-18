from containers.core.base import FrozenSequence, BaseSequence, BaseSet
from containers.core.common import reduce


class SequenceSet(BaseSequence, BaseSet):
    def __init__(self, iterable=()):
        BaseSequence.__init__(self, iterable=iterable)

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
        if index:
            self._delete_item(index=index)


class OrderedSet(SequenceSet):
    """
    use sequence set for ordered set
    """


class OrderedFrozenSet(FrozenSequence):
    def __init__(self, iterable=()):
        iterable = reduce(iterable)
        super().__init__(iterable=reduce(iterable))
