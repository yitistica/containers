

class BaseView(object):
    """
    view: ?
    """
    def __init__(self, *args, **kwargs):
        pass


class Iterable(BaseView):
    """
    base view for an iterable
    """
    def __init__(self, iterable):
        self._iterable = iterable
        super().__init__()

    @property
    def iterable(self):
        return self._iterable

    @property
    def size(self):
        return NotImplemented
