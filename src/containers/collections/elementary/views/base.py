from containers.core.base import reinstantiate_iterable


class ViewBase(object):
    pass


class LocationIterator(object):
    def __init__(self, locator_iterator):
        self._iterator = locator_iterator

    def __iter__(self):
        return self

    def __next__(self):
        item = self._iterator.__next__()
        return item


class IterableView(ViewBase):
    """
    a view that wraps around the iterable and has the following methods:
        a. iterable, iter_loc, and iter.
    the aim of the wrap-around is to provide:
    """
    def __init__(self, iterable):
        self._iterable = iterable
        super().__init__()

    @property
    def iterable(self):
        return self._iterable

    def iter_loc(self, *args, **kwargs):
        return NotImplemented

    def iter(self, *args, **kwargs):
        loc_iterator = self.iter_loc(*args, **kwargs)
        for loc in loc_iterator:
            yield loc, self.iterable[loc]

    @property
    def size(self):
        return len(self._iterable)

    def __getitem__(self, item):
        return self.iterable[item]

    def reinstantiate(self, iterable):
        return reinstantiate_iterable(obj=self._iterable, iterable=iterable)
