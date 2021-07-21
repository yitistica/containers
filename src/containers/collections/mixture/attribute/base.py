from containers.core.base import BaseMap
from containers.core.elemental import ImmutableKey, Value
from dataclasses import dataclass


class AttrKey(ImmutableKey):
    pass


class AttrValue(Value):
    pass


class AttributeBase(BaseMap):
    def __init__(self, attributes=()):
        super().__init__(iterable=attributes)
        self._attrs = self._mapping

    @property
    def attrs(self):
        return self._attrs


