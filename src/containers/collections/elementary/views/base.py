"""
given one iterable:
    build two iterator:
        locator:
        value:

any iterator based view: should be able to be shared between mapping and sequence;

only need an iterator to loop over

locator based view:

multiple indices

view has get method, multiple gets, and inter

"""
from containers.collections.elementary.views.sequential import IndexIterator


class ViewBase(object):
    def __init__(self, *args, **kwargs):
        pass


class LocationIterator(object):
    def __init__(self, locator_iterator):
        self._iterator = locator_iterator  # keys()

    def __iter__(self):
        return self

    def __next__(self):
        item = self._iterator.__next__()
        return item


class IterableWrapView(ViewBase):
    """
    base view for an iterable
    """
    def __init__(self, iterable):
        self._iterable = iterable
        super().__init__()

    @property
    def iterable(self):
        return self._iterable

    def locator(self):
        return NotImplemented

    def value(self):
        return NotImplemented

    @property
    def size(self):
        return NotImplemented


class IterLocatorView(IterableWrapView):
    def __init__(self, iterable=(), **kwargs):
        super().__init__(iterable=iterable)
        self._iterator = IndexIterator(self.size, **kwargs)

    def __iter__(self):
        return self

    def __next__(self):
        index = self._iterator.__next__()
        return index, self.iterable[index]


class IterMappingView(object):

    def __init__(self, mapping):
        self._mapping = mapping
        self.key = iter(mapping.keys())
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        key = self.key.__next__()


class SequenceViewBase(IterableWrapView):
    def __init__(self, sequence=()):
        super().__init__(iterable=sequence)

    @property
    def size(self):
        return len(self.iterable)


a  = {1:2, 2:3, 3:4}
b = LocationIterator(a.keys())

for i in b:
    print(i)


class IterIndexView(SequenceViewBase):
    def __init__(self, iterable=(), **kwargs):
        super().__init__(sequence=iterable)
        self._index_iterator = IndexIterator(self.size, **kwargs)

    def __iter__(self):
        return self

    def __next__(self):
        index = self._index_iterator.__next__()
        return index, self.iterable[index]