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