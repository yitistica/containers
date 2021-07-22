from containers.core.base import BaseSequence


class InvalidCategoryValueError(Exception):
    def __init__(self, value, category):
        message = f'Given value {value} is not of part of <{category}> .'
        super().__init__(message)


class CategorySequence(BaseSequence):
    """
    """
    def __init__(self, categories):

        super().__init__()

    def _set_item(self, index, value):

        self._list[index] = value


class RecursiveView(object):
    pass


class StatisticsView(object):
    pass

    def apply(self):
        pass

    def count(self):
        pass


class SetView(object):
    pass


class FilterView(object):
    pass


class MapView(object):
    pass


class GroupView(object):
    pass


class LocationView(object):

    def __getitem__(self, item):
        # apply a function;
        pass


class RandomView(object):
    pass



class XList(BaseSequence, RecursiveView):
    """a sequence without end"""
    pass

    @property
    def repeat(self):
        return None

