"""
TreeDict: a mix of sequences and elementary;
"""
from containers.collections.elementary.dicts import Dict



class TreeDict(Dict):
    def __init__(self, iterable):
        super().__init__(iterable=iterable)

    @property
    def loc(self):
        return

    @property
    def get_loc(self):
        return