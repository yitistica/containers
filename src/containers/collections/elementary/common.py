"""
with dict.efilter(filter=True) as  filter, k, v:
    condtion_1 = lambda x: x > 2
    a = filter(conditon, select=)
"""


class IterView(object):
    pass


class ApplyView(object):
    pass


class BoolFilterView(object):
    """only for """
    pass


class FilterView(object):
    pass


class GroupView(object):
    pass


class ElementView(object):
    def __init__(self, type_, iterable):
        self._type = type_
        self._iterable = iterable


class EFilterView(object):
    pass


