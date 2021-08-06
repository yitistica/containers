

class IndexIterable(object):

    def __init__(self, size):
        self._size = size




class SliceIter(object):
    def __init__(self, slice_, size):
        assert isinstance(slice_, slice)
        self._slice = slice_
        assert isinstance(size, int) and (size >= 0)
        self._size = size
        self._from, self._to, self._step = self._parse_slice(slice_=slice_, size=size)

        self._current_step = self._from

    @staticmethod
    def _parse_slice(slice_, size):
        start, stop, step = slice_.indices(size)
        return start, stop, step

    def __iter__(self):
        return self

    def __next__(self):
        if self._current_step >= self._to:
            raise StopIteration
        else:
            current_step = self._current_step
            self._current_step += self._step
            return current_step


class MixedSliceIndexIter(object):
    def __init__(self, indices, size):
        self._indices = indices

        assert isinstance(size, int) and (size >= 0)
        self._size = size

    def __iter__(self):
        for index in self._indices:
            if isinstance(index, slice):
                _slice_iter = SliceIter(index, size=self._size)
                for sub_index in _slice_iter:
                    yield sub_index
            else:
                yield index
