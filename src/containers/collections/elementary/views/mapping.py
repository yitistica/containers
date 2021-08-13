"""
both key and value
"""
from containers.collections.elementary.views.base import LocationIterator


class MappingLocationIterator(LocationIterator):

    def __init__(self, mapping):
        locator_iterator = iter(mapping.keys())
        super().__init__(locator_iterator=locator_iterator)